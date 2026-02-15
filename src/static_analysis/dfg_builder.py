"""
Data Flow Graph builder.

Purpose:
- Build DFGs from AST trees
- Track variable definitions and uses
- Enable semantic understanding and test assertion inference
"""

from typing import Dict, List, Optional, Set
import uuid
import javalang
import logging

from static_analysis.ast_model import ASTTree, ASTNode
from static_analysis.dfg_model import DFGNode, DFGEdge, DataFlowGraph

logger = logging.getLogger(__name__)

class DFGBuilder:
    """
    Base DFG builder abstraction.
    """

    def build(self, ast_tree: ASTTree) -> List[DataFlowGraph]:
        raise NotImplementedError


# =========================
# Python DFG Builder
# =========================

class PythonDFGBuilder(DFGBuilder):
    """
    Simplified Python DFG builder.
    """

    def build(self, ast_tree: ASTTree) -> List[DataFlowGraph]:
        graphs: List[DataFlowGraph] = []

        for node in ast_tree.root.children:
            if node.node_type in ("FunctionDef", "AsyncFunctionDef"):
                graphs.append(self._build_function_dfg(node, ast_tree))

        return graphs

    def _build_function_dfg(
        self,
        func_node: ASTNode,
        ast_tree: ASTTree
    ) -> DataFlowGraph:
        nodes: Dict[str, DFGNode] = {}
        edges: List[DFGEdge] = {}
        edges = []

        last_def: Dict[str, str] = {}

        for stmt in func_node.children:
            self._process_statement(stmt, nodes, edges, last_def)

        return DataFlowGraph(
            graph_id=f"{ast_tree.file_path}:{func_node.name}",
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            metadata={"type": "function"}
        )

    def _process_statement(
        self,
        stmt: ASTNode,
        nodes: Dict[str, DFGNode],
        edges: List[DFGEdge],
        last_def: Dict[str, str]
    ) -> None:
        if stmt.node_type == "Assign":
            target = stmt.attributes.get("targets", [None])[0]
            value = stmt.attributes.get("value")

            if isinstance(target, str):
                node_id = self._new_id()
                nodes[node_id] = DFGNode(
                    node_id=node_id,
                    variable=target,
                    operation="DEFINE"
                )

                if target in last_def:
                    edges.append(
                        DFGEdge(
                            source=last_def[target],
                            target=node_id,
                            label=target
                        )
                    )

                last_def[target] = node_id

        elif stmt.node_type == "Name":
            var = stmt.attributes.get("id")
            if var and var in last_def:
                use_id = self._new_id()
                nodes[use_id] = DFGNode(
                    node_id=use_id,
                    variable=var,
                    operation="USE"
                )
                edges.append(
                    DFGEdge(
                        source=last_def[var],
                        target=use_id,
                        label=var
                    )
                )

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# ============================================================
# Expected ASTTree Contract (from ast_parser stage)
# ============================================================
# ASTTree:
#   - language: str
#   - file_path: str
#   - root: javalang AST root

# ============================================================
# JavaDFGBuilder (Factory-Compatible + ASTNode Traversal)
# ============================================================

class JavaDFGBuilder:
    """
    Factory-compatible Java DFG builder.

    Assumes ASTTree.root is a normalized ASTNode model:
        ASTNode:
            - node_type: str
            - name: Optional[str]
            - children: List[ASTNode]
            - attributes: Dict[str, Any]
            - line: Optional[int]
    """    

    def __init__(self):
        self.language = "java"

    # --------------------------------------------------------
    # Public Entry
    # --------------------------------------------------------

    def build(self, ast_tree) -> List[DataFlowGraph]:

        if ast_tree.language.lower() != "java":
            raise ValueError(
                f"JavaDFGBuilder cannot process language={ast_tree.language}"
            )

        graphs: List[DataFlowGraph] = []

        methods = self._collect_methods(ast_tree.root)

        logger.info(
            "JavaDFGBuilder: Methods discovered",
            extra={
                "file_path": ast_tree.file_path,
                "method_count": len(methods)
            }
        )

        for method_node in methods:
            graph = self._build_method_dfg(
                method_node,
                ast_tree.file_path
            )
            graphs.append(graph)

        return graphs

    # --------------------------------------------------------
    # AST Traversal (NO .filter())
    # --------------------------------------------------------

    def _collect_methods(self, node) -> List:
        methods = []

        if node.node_type == "MethodDeclaration":
            methods.append(node)

        for child in getattr(node, "children", []) or []:
            methods.extend(self._collect_methods(child))

        return methods

    # --------------------------------------------------------
    # Per-Method DFG
    # --------------------------------------------------------

    def _build_method_dfg(self, method_node, file_path: str) -> DataFlowGraph:

        method_name = method_node.name
        graph_id = self._generate_graph_id(file_path, method_name)

        graph = DataFlowGraph(
            graph_id=graph_id,
            language=self.language,
            method_id=method_name,
            metadata={"file_path": file_path}
        )

        definition_map: Dict[str, DFGNode] = {}

        logger.info(
            "Building Java DFG",
            extra={
                "file_path": file_path,
                "method_id": method_name,
                "graph_id": graph_id
            }
        )

        # ----------------------------------------------------
        # Parameters
        # ----------------------------------------------------
        parameters = method_node.attributes.get("parameters", [])

        for param in parameters:
            param_node = self._create_node(
                variable_name=param.get("name"),
                kind="parameter",
                method_id=method_name,
                line=method_node.line
            )
            graph.nodes.append(param_node)
            definition_map[param.get("name")] = param_node

        # ----------------------------------------------------
        # Traverse method body
        # ----------------------------------------------------
        for child in method_node.children:
            self._process_node(
                child,
                method_name,
                graph,
                definition_map
            )

        logger.info(
            "Java DFG constructed",
            extra={
                "graph_id": graph_id,
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges)
            }
        )

        return graph

    # --------------------------------------------------------
    # Generic ASTNode Processing
    # --------------------------------------------------------

    def _process_node(
        self,
        node,
        method_id: str,
        graph: DataFlowGraph,
        definition_map: Dict[str, DFGNode]
    ):

        if node.node_type == "VariableDeclarator":
            var_name = node.name

            def_node = self._create_node(
                variable_name=var_name,
                kind="definition",
                method_id=method_id,
                line=self._resolve_line(node, fallback=node.parent.line)
            )
            graph.nodes.append(def_node)
            definition_map[var_name] = def_node

        elif node.node_type == "Assignment":
            var_name = node.attributes.get("left")

            def_node = self._create_node(
                variable_name=var_name,
                kind="definition",
                method_id=method_id,
                line=node.line
            )
            graph.nodes.append(def_node)
            definition_map[var_name] = def_node

        elif node.node_type == "MemberReference":
            var_name = node.name

            use_node = self._create_node(
                variable_name=var_name,
                kind="usage",
                method_id=method_id,
                line=node.line
            )
            graph.nodes.append(use_node)

            if var_name in definition_map:
                self._create_edge(
                    definition_map[var_name],
                    use_node,
                    graph
                )

        elif node.node_type == "ReturnStatement":
            return_node = self._create_node(
                variable_name="return",
                kind="return",
                method_id=method_id,
                line=node.line
            )
            graph.nodes.append(return_node)

        # Recurse
        for child in getattr(node, "children", []) or []:
            self._process_node(
                child,
                method_id,
                graph,
                definition_map
            )

    # --------------------------------------------------------
    # Utilities
    # --------------------------------------------------------
    def _resolve_line(self, node, fallback=None):
        current = node
        while current:
            if current.line:
                return current.line
            current = current.parent
        return fallback

    def _create_node(
        self,
        variable_name: str,
        kind: str,
        method_id: str,
        line: Optional[int]
    ) -> DFGNode:
        return DFGNode(
            node_id=str(uuid.uuid4()),
            variable_name=variable_name,
            kind=kind,
            method_id=method_id,
            line=line
        )

    def _create_edge(
        self,
        source: DFGNode,
        target: DFGNode,
        graph: DataFlowGraph
    ):
        graph.edges.append(
            DFGEdge(
                edge_id=str(uuid.uuid4()),
                source_node_id=source.node_id,
                target_node_id=target.node_id,
                relation="flows_to"
            )
        )

    def _generate_graph_id(self, file_path: str, method_name: str) -> str:
        base = f"{file_path}:{method_name}:dfg"
        return str(uuid.uuid5(uuid.NAMESPACE_DNS, base))


# =========================
# Builder Factory
# =========================

class DFGBuilderFactory:
    """
    Factory for selecting DFG builder by language.
    """

    _builders = {
        "Python": PythonDFGBuilder(),
        "Java": JavaDFGBuilder()
    }

    @classmethod
    def get_builder(cls, language: str) -> DFGBuilder:
        if language not in cls._builders:
            raise ValueError(f"No DFG builder available for language: {language}")
        return cls._builders[language]


def build_dfg(ast_tree: ASTTree) -> List[DataFlowGraph]:
    """
    Functional entry point for DFG generation.
    """
    builder = DFGBuilderFactory.get_builder(ast_tree.language)
    return builder.build(ast_tree)
