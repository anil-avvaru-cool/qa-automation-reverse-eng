"""
Control Flow Graph builder.

Purpose:
- Build CFGs from normalized AST trees
- Provide structured control-flow for semantic analysis
- Enable path-based test generation
"""

from typing import Dict, List, Optional
import uuid
import logging
import javalang

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
    Intra-procedural Control Flow Graph builder for Java (javalang AST).
    """

    def build(self, ast_tree: ASTTree) -> List[ControlFlowGraph]:
        cfgs: List[ControlFlowGraph] = []
        current_class: Optional[str] = None

        def method_id(class_name: Optional[str], method_name: str) -> str:
            return f"{class_name}.{method_name}" if class_name else method_name

        def visit(node: ASTNode):
            nonlocal current_class

            if node.node_type == "ClassDeclaration":
                current_class = node.name

            elif node.node_type in ("MethodDeclaration", "ConstructorDeclaration"):
                mid = method_id(current_class, node.name)
                cfg = self._build_method_cfg(ast_tree, mid, node)
                cfgs.append(cfg)

            for child in node.children or []:
                visit(child)

            if node.node_type == "ClassDeclaration":
                current_class = None

        visit(ast_tree.root)
        return cfgs

    # ------------------------------------------------------------------
    # Method-level CFG
    # ------------------------------------------------------------------

    def _build_method_cfg(
        self,
        ast_tree: ASTTree,
        method_id: str,
        method_node: ASTNode
    ) -> ControlFlowGraph:

        graph_id = f"{method_id}_cfg"

        nodes: Dict[str, CFGNode] = {}
        edges: List[CFGEdge] = []
        exit_nodes: List[str] = []

        def new_id() -> str:
            return str(uuid.uuid4())

        def add_node(node_type: str, label: str, metadata=None) -> str:
            nid = new_id()
            nodes[nid] = CFGNode(
                node_id=nid,
                node_type=node_type,
                label=label,
                metadata=metadata or {}
            )
            return nid

        def add_edge(src: str, tgt: str, edge_type="normal"):
            edges.append(
                CFGEdge(
                    source=src,
                    target=tgt,
                    edge_type=edge_type
                )
            )

        def connect(srcs: List[str], tgt: str):
            for s in srcs:
                add_edge(s, tgt)

        # --------------------------------------------------------------
        # ENTRY
        # --------------------------------------------------------------

        entry_id = add_node("ENTRY", "ENTRY")
        current_exits = [entry_id]

        # --------------------------------------------------------------
        # Statement Processing
        # --------------------------------------------------------------

        def process_statement(stmt: ASTNode, incoming: List[str]) -> List[str]:
            stype = stmt.node_type

            # ---- IF ----
            if stype == "IfStatement":
                cond_id = add_node("CONDITION", "if")
                connect(incoming, cond_id)

                then_block = stmt.children[1] if len(stmt.children) > 1 else None
                else_block = stmt.children[2] if len(stmt.children) > 2 else None

                then_exits = process_block(then_block, [cond_id])
                else_exits = process_block(else_block, [cond_id]) if else_block else []

                return then_exits + else_exits or [cond_id]

            # ---- RETURN ----
            if stype == "ReturnStatement":
                ret_id = add_node("RETURN", "return")
                connect(incoming, ret_id)
                exit_nodes.append(ret_id)
                return []

            # ---- GENERIC STATEMENT ----
            stmt_id = add_node("STATEMENT", stype)
            connect(incoming, stmt_id)
            return [stmt_id]

        def process_block(block: Optional[ASTNode], incoming: List[str]) -> List[str]:
            if not block:
                return incoming

            exits = incoming
            for stmt in block.children or []:
                exits = process_statement(stmt, exits)
            return exits

        # --------------------------------------------------------------
        # Locate Method Body
        # --------------------------------------------------------------

        body = next(
            (c for c in method_node.children or [] if c.node_type == "BlockStatement"),
            None
        )

        if body:
            current_exits = process_block(body, current_exits)

        # --------------------------------------------------------------
        # EXIT handling
        # --------------------------------------------------------------

        if not exit_nodes:
            exit_nodes = current_exits

        return ControlFlowGraph(
            graph_id=graph_id,
            language=ast_tree.language,
            method_id=method_id,
            nodes=nodes,
            edges=edges,
            entry_node=entry_id,
            exit_nodes=list(set(exit_nodes)),
            metadata={
                "file_path": ast_tree.file_path,
                "builder": "JavaCFGBuilder"
            }
        )



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
    logger = logging.getLogger(__name__)
    logger.info(f"Building CFG for file: {ast_tree.file_path} with language: {ast_tree.language}")
    return builder.build(ast_tree)
