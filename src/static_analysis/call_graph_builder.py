"""
Call Graph builder.

Purpose:
- Build inter-procedural call graphs from AST
- Enable impact analysis and end-to-end test generation
"""

from typing import Dict, List
import uuid
import logging

from static_analysis.ast_model import ASTTree, ASTNode
from static_analysis.call_graph_model import (
    CallGraph,
    CallGraphNode,
    CallGraphEdge,
)


class CallGraphBuilder:
    """
    Base call graph builder abstraction.
    """

    def build(self, ast_tree: ASTTree) -> CallGraph:
        raise NotImplementedError


# =========================
# Python Call Graph Builder
# =========================

class PythonCallGraphBuilder(CallGraphBuilder):
    """
    Static Python call graph builder (best-effort).
    """

    def build(self, ast_tree: ASTTree) -> CallGraph:
        nodes: Dict[str, CallGraphNode] = {}
        edges: List[CallGraphEdge] = []

        functions = self._collect_functions(ast_tree)

        for func_id, func_node in functions.items():
            for call_name in self._find_calls(func_node):
                if call_name in functions:
                    edges.append(
                        CallGraphEdge(
                            caller=func_id,
                            callee=functions[call_name],
                            call_type="direct"
                        )
                    )

        entry_points = self._detect_entry_points(functions)

        return CallGraph(
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            entry_points=entry_points,
            metadata={"type": "static"}
        )

    def _collect_functions(
        self,
        ast_tree: ASTTree
    ) -> Dict[str, str]:
        functions: Dict[str, str] = {}

        for node in ast_tree.root.children:
            if node.node_type in ("FunctionDef", "AsyncFunctionDef"):
                node_id = self._new_id()
                functions[node.name] = node_id

        return functions

    def _find_calls(self, func_node: ASTNode) -> List[str]:
        calls: List[str] = []

        def walk(node: ASTNode):
            if node.node_type == "Call":
                func_name = node.attributes.get("func")
                if isinstance(func_name, str):
                    calls.append(func_name)
            for child in node.children:
                walk(child)

        walk(func_node)
        return calls

    def _detect_entry_points(self, functions: Dict[str, str]) -> List[str]:
        return [
            node_id
            for name, node_id in functions.items()
            if name == "main"
        ]

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Java Call Graph Builder
# =========================

class JavaCallGraphBuilder(CallGraphBuilder):
    """
    Static Java call graph builder (best-effort).
    """
    logger = logging.getLogger(__name__)

    def build(self, ast_tree: ASTTree) -> CallGraph:
        nodes: Dict[str, CallGraphNode] = {}
        edges: List[CallGraphEdge] = []

        methods = self._collect_methods(ast_tree)

        for caller_name, caller_id in methods.items():
            self.logger.info(f"Building call graph for caller_name: {caller_name} and caller_id: {caller_id}")
            for callee_name in self._find_calls(ast_tree):
                if callee_name in methods:
                    edges.append(
                        CallGraphEdge(
                            caller=caller_id,
                            callee=methods[callee_name],
                            call_type="static"
                        )
                    )

        entry_points = [
            node_id for name, node_id in methods.items()
            if name == "main"
        ]

        return CallGraph(
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            entry_points=entry_points,
            metadata={"type": "static"}
        )

    def _collect_methods(
        self,
        ast_tree: ASTTree
    ) -> Dict[str, str]:
        methods: Dict[str, str] = {}

        for first_level_node in ast_tree.root.children:
            if first_level_node.node_type == "ClassDeclaration":
                self.logger.info(f"Building call graph for ClassDeclaration: {first_level_node.name}")
                for second_level_node in first_level_node.children:
                    if second_level_node.node_type == "MethodDeclaration":
                        self.logger.info(f"Building call graph for MethodDeclaration: {second_level_node.name}")
                        methods[second_level_node.name] = self._new_id()        

        return methods

    def _find_calls(self, ast_tree: ASTTree) -> List[str]:
        calls: List[str] = []

        def walk(node: ASTNode):
            if node.node_type in ("MethodInvocation", "SuperMethodInvocation"):
                qualifier = node.attributes["qualifier"] or ""
                member = node.attributes["member"] 
                method_invocation = f"{qualifier}.{member}" if qualifier else member                
                self.logger.info(f"Building call graph for MethodInvocation: {method_invocation}")
                calls.append(method_invocation)
            for child in node.children:
                walk(child)

        walk(ast_tree.root)
        return calls

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Builder Factory
# =========================

class CallGraphBuilderFactory:
    """
    Factory for selecting call graph builder by language.
    """

    _builders = {
        "Python": PythonCallGraphBuilder(),
        "Java": JavaCallGraphBuilder()
    }

    @classmethod
    def get_builder(cls, language: str) -> CallGraphBuilder:
        if language not in cls._builders:
            raise ValueError(
                f"No call graph builder available for language: {language}"
            )
        return cls._builders[language]


def build_call_graph(ast_tree: ASTTree) -> CallGraph:
    """
    Functional entry point for call graph generation.
    """
    builder = CallGraphBuilderFactory.get_builder(ast_tree.language)
    return builder.build(ast_tree)
