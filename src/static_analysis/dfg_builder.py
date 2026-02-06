"""
Data Flow Graph builder.

Purpose:
- Build DFGs from AST trees
- Track variable definitions and uses
- Enable semantic understanding and test assertion inference
"""

from typing import Dict, List
import uuid

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


# =========================
# Java DFG Builder
# =========================

class JavaDFGBuilder(DFGBuilder):
    """
    Simplified Java DFG builder.
    """

    def build(self, ast_tree: ASTTree) -> List[DataFlowGraph]:
        graphs: List[DataFlowGraph] = []

        for node in ast_tree.root.children:
            if node.node_type == "MethodDeclaration":
                graphs.append(self._build_method_dfg(node, ast_tree))

        return graphs

    def _build_method_dfg(
        self,
        method_node: ASTNode,
        ast_tree: ASTTree
    ) -> DataFlowGraph:
        nodes: Dict[str, DFGNode] = {}
        edges: List[DFGEdge] = []
        last_def: Dict[str, str] = {}

        for stmt in method_node.children:
            self._process_statement(stmt, nodes, edges, last_def)

        return DataFlowGraph(
            graph_id=f"{ast_tree.file_path}:{method_node.name}",
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            metadata={"type": "method"}
        )

    def _process_statement(
        self,
        stmt: ASTNode,
        nodes: Dict[str, DFGNode],
        edges: List[DFGEdge],
        last_def: Dict[str, str]
    ) -> None:
        if stmt.node_type == "VariableDeclarator":
            var = stmt.name
            node_id = self._new_id()
            nodes[node_id] = DFGNode(
                node_id=node_id,
                variable=var,
                operation="DEFINE"
            )
            last_def[var] = node_id

        elif stmt.node_type == "MemberReference":
            var = stmt.name
            if var in last_def:
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
