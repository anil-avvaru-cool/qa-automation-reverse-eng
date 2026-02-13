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

from static_analysis.ast_model import ASTTree, ASTNode
from static_analysis.dfg_model import DFGNode, DFGEdge, DataFlowGraph


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
# Java DFG Builder (Factory Compatible)
# ============================================================

class JavaDFGBuilder:
    """
    Factory-compatible, stateless Java DFG builder.

    Entry:
        build(ast_tree) -> List[DataFlowGraph]

    Scope:
        Intra-procedural only.
        One DFG per MethodDeclaration.
    """

    def __init__(self):
        self.language = "java"

    # --------------------------------------------------------
    # Public API
    # --------------------------------------------------------

    def build(self, ast_tree) -> List[DataFlowGraph]:
        """
        Build DFGs for all methods inside a Java ASTTree.
        """

        if ast_tree.language.lower() != "java":
            raise ValueError(
                f"JavaDFGBuilder cannot process language={ast_tree.language}"
            )

        root = ast_tree.root
        file_path = ast_tree.file_path

        graphs: List[DataFlowGraph] = []

        for _, node in root.filter(javalang.tree.MethodDeclaration):
            graph = self._build_method_dfg(node, file_path)
            graphs.append(graph)

        logger.info(
            "Java DFG build complete",
            extra={
                "file_path": file_path,
                "total_methods": len(graphs)
            }
        )

        return graphs

    # --------------------------------------------------------
    # Per-Method Builder
    # --------------------------------------------------------

    def _build_method_dfg(
        self,
        method_node: javalang.tree.MethodDeclaration,
        file_path: str
    ) -> DataFlowGraph:

        graph_id = self._generate_graph_id(file_path, method_node.name)

        graph = DataFlowGraph(
            graph_id=graph_id,
            language=self.language,
            method_id=method_node.name,
            metadata={"file_path": file_path}
        )

        logger.info(
            "Building Java DFG for method",
            extra={
                "file_path": file_path,
                "method_id": method_node.name,
                "graph_id": graph_id
            }
        )

        definition_map: Dict[str, DFGNode] = {}

        # ----------------------------------------------------
        # Parameters → definition nodes
        # ----------------------------------------------------
        if method_node.parameters:
            for param in method_node.parameters:
                param_node = self._create_node(
                    variable_name=param.name,
                    kind="parameter",
                    method_id=method_node.name,
                    line=self._safe_line(param)
                )
                graph.nodes.append(param_node)
                definition_map[param.name] = param_node

        # ----------------------------------------------------
        # Process method body
        # ----------------------------------------------------
        if method_node.body:
            for statement in method_node.body:
                self._process_statement(
                    statement,
                    method_node.name,
                    graph,
                    definition_map
                )

        logger.info(
            "Java DFG constructed",
            extra={
                "graph_id": graph_id,
                "method_id": method_node.name,
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges)
            }
        )

        return graph

    # --------------------------------------------------------
    # Statement Processing
    # --------------------------------------------------------

    def _process_statement(
        self,
        statement,
        method_id: str,
        graph: DataFlowGraph,
        definition_map: Dict[str, DFGNode]
    ):

        if isinstance(statement, javalang.tree.LocalVariableDeclaration):
            for declarator in statement.declarators:
                def_node = self._create_node(
                    variable_name=declarator.name,
                    kind="definition",
                    method_id=method_id,
                    line=self._safe_line(statement)
                )
                graph.nodes.append(def_node)
                definition_map[declarator.name] = def_node

                if declarator.initializer:
                    self._process_expression(
                        declarator.initializer,
                        method_id,
                        graph,
                        definition_map,
                        target_node=def_node
                    )

        elif isinstance(statement, javalang.tree.StatementExpression):
            self._process_expression(
                statement.expression,
                method_id,
                graph,
                definition_map
            )

        elif isinstance(statement, javalang.tree.ReturnStatement):
            if statement.expression:
                return_node = self._create_node(
                    variable_name="return",
                    kind="return",
                    method_id=method_id,
                    line=self._safe_line(statement)
                )
                graph.nodes.append(return_node)

                self._process_expression(
                    statement.expression,
                    method_id,
                    graph,
                    definition_map,
                    target_node=return_node
                )

        elif hasattr(statement, "statements") and statement.statements:
            for nested in statement.statements:
                self._process_statement(
                    nested,
                    method_id,
                    graph,
                    definition_map
                )

    # --------------------------------------------------------
    # Expression Processing
    # --------------------------------------------------------

    def _process_expression(
        self,
        expression,
        method_id: str,
        graph: DataFlowGraph,
        definition_map: Dict[str, DFGNode],
        target_node: Optional[DFGNode] = None
    ):

        if isinstance(expression, javalang.tree.Assignment):
            left = expression.expressionl
            right = expression.value

            if isinstance(left, javalang.tree.MemberReference):
                var_name = left.member

                def_node = self._create_node(
                    variable_name=var_name,
                    kind="definition",
                    method_id=method_id,
                    line=self._safe_line(expression)
                )
                graph.nodes.append(def_node)
                definition_map[var_name] = def_node

                self._process_expression(
                    right,
                    method_id,
                    graph,
                    definition_map,
                    target_node=def_node
                )

        elif isinstance(expression, javalang.tree.MemberReference):
            var_name = expression.member

            use_node = self._create_node(
                variable_name=var_name,
                kind="usage",
                method_id=method_id,
                line=self._safe_line(expression)
            )
            graph.nodes.append(use_node)

            if var_name in definition_map:
                self._create_edge(
                    definition_map[var_name],
                    use_node,
                    graph
                )

            if target_node:
                self._create_edge(
                    use_node,
                    target_node,
                    graph
                )

        elif hasattr(expression, "children"):
            for child in expression.children:
                if child:
                    self._process_expression(
                        child,
                        method_id,
                        graph,
                        definition_map,
                        target_node
                    )

    # --------------------------------------------------------
    # Utilities
    # --------------------------------------------------------

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

    def _safe_line(self, node) -> Optional[int]:
        if hasattr(node, "position") and node.position:
            return node.position.line
        return None



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
