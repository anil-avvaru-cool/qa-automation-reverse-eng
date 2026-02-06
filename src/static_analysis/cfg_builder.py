"""
Control Flow Graph builder.

Purpose:
- Build CFGs from normalized AST trees
- Provide structured control-flow for semantic analysis
- Enable path-based test generation
"""

from typing import Dict, List
import uuid

from static_analysis.ast_model import ASTTree, ASTNode
from static_analysis.cfg_model import CFGNode, CFGEdge, ControlFlowGraph


class CFGBuilder:
    """
    Base CFG builder abstraction.
    """

    def build(self, ast_tree: ASTTree) -> List[ControlFlowGraph]:
        raise NotImplementedError


# =========================
# Python CFG Builder
# =========================

class PythonCFGBuilder(CFGBuilder):
    """
    Simplified Python CFG builder.
    """

    def build(self, ast_tree: ASTTree) -> List[ControlFlowGraph]:
        graphs: List[ControlFlowGraph] = []

        for node in ast_tree.root.children:
            if node.node_type in ("FunctionDef", "AsyncFunctionDef"):
                graphs.append(self._build_function_cfg(node, ast_tree))

        return graphs

    def _build_function_cfg(
        self,
        func_node: ASTNode,
        ast_tree: ASTTree
    ) -> ControlFlowGraph:
        nodes: Dict[str, CFGNode] = {}
        edges: List[CFGEdge] = []

        entry_id = self._new_id()
        exit_id = self._new_id()

        nodes[entry_id] = CFGNode(
            node_id=entry_id,
            node_type="ENTRY",
            label=func_node.name
        )

        prev_id = entry_id

        for stmt in func_node.children:
            stmt_id = self._new_id()
            nodes[stmt_id] = CFGNode(
                node_id=stmt_id,
                node_type=stmt.node_type,
                metadata={"ast_type": stmt.node_type}
            )
            edges.append(CFGEdge(source=prev_id, target=stmt_id))
            prev_id = stmt_id

        nodes[exit_id] = CFGNode(
            node_id=exit_id,
            node_type="EXIT"
        )
        edges.append(CFGEdge(source=prev_id, target=exit_id))

        return ControlFlowGraph(
            graph_id=f"{ast_tree.file_path}:{func_node.name}",
            language=ast_tree.language,
            entry_node=entry_id,
            exit_nodes=[exit_id],
            nodes=nodes,
            edges=edges,
            metadata={"type": "function"}
        )

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Java CFG Builder
# =========================

class JavaCFGBuilder(CFGBuilder):
    """
    Simplified Java CFG builder.
    """

    def build(self, ast_tree: ASTTree) -> List[ControlFlowGraph]:
        graphs: List[ControlFlowGraph] = []

        for node in ast_tree.root.children:
            if node.node_type == "MethodDeclaration":
                graphs.append(self._build_method_cfg(node, ast_tree))

        return graphs

    def _build_method_cfg(
        self,
        method_node: ASTNode,
        ast_tree: ASTTree
    ) -> ControlFlowGraph:
        nodes: Dict[str, CFGNode] = {}
        edges: List[CFGEdge] = []

        entry_id = self._new_id()
        exit_id = self._new_id()

        nodes[entry_id] = CFGNode(
            node_id=entry_id,
            node_type="ENTRY",
            label=method_node.name
        )

        prev_id = entry_id

        for stmt in method_node.children:
            stmt_id = self._new_id()
            nodes[stmt_id] = CFGNode(
                node_id=stmt_id,
                node_type=stmt.node_type,
                metadata={"ast_type": stmt.node_type}
            )
            edges.append(CFGEdge(source=prev_id, target=stmt_id))
            prev_id = stmt_id

        nodes[exit_id] = CFGNode(
            node_id=exit_id,
            node_type="EXIT"
        )
        edges.append(CFGEdge(source=prev_id, target=exit_id))

        return ControlFlowGraph(
            graph_id=f"{ast_tree.file_path}:{method_node.name}",
            language=ast_tree.language,
            entry_node=entry_id,
            exit_nodes=[exit_id],
            nodes=nodes,
            edges=edges,
            metadata={"type": "method"}
        )

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Builder Factory
# =========================

class CFGBuilderFactory:
    """
    Factory for selecting CFG builder by language.
    """

    _builders = {
        "Python": PythonCFGBuilder(),
        "Java": JavaCFGBuilder()
    }

    @classmethod
    def get_builder(cls, language: str) -> CFGBuilder:
        if language not in cls._builders:
            raise ValueError(f"No CFG builder available for language: {language}")
        return cls._builders[language]


def build_cfg(ast_tree: ASTTree) -> List[ControlFlowGraph]:
    """
    Functional entry point for CFG generation.
    """
    builder = CFGBuilderFactory.get_builder(ast_tree.language)
    return builder.build(ast_tree)
