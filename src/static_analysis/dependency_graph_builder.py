"""
Dependency Graph builder.

Purpose:
- Build module/package dependency graphs from AST
- Capture import and include relationships
- Enable impact and ownership analysis
"""

from typing import Dict, List
import uuid

from static_analysis.ast_model import ASTTree, ASTNode
from static_analysis.dependency_graph_model import (
    DependencyGraph,
    DependencyNode,
    DependencyEdge,
)


class DependencyGraphBuilder:
    """
    Base dependency graph builder abstraction.
    """

    def build(self, ast_tree: ASTTree) -> DependencyGraph:
        raise NotImplementedError


# =========================
# Python Dependency Builder
# =========================

class PythonDependencyGraphBuilder(DependencyGraphBuilder):
    """
    Dependency graph builder for Python.
    """

    def build(self, ast_tree: ASTTree) -> DependencyGraph:
        nodes: Dict[str, DependencyNode] = {}
        edges: List[DependencyEdge] = []

        file_node_id = self._new_id()
        nodes[file_node_id] = DependencyNode(
            node_id=file_node_id,
            name=ast_tree.file_path,
            node_type="module",
            file_path=ast_tree.file_path,
            language=ast_tree.language,
        )

        for node in ast_tree.root.children:
            if node.node_type == "Import":
                for name in node.attributes.get("names", []):
                    self._add_dependency(
                        source_id=file_node_id,
                        target_name=name,
                        nodes=nodes,
                        edges=edges,
                        dep_type="import",
                        language=ast_tree.language
                    )

            elif node.node_type == "ImportFrom":
                module = node.attributes.get("module")
                if module:
                    self._add_dependency(
                        source_id=file_node_id,
                        target_name=module,
                        nodes=nodes,
                        edges=edges,
                        dep_type="import",
                        language=ast_tree.language
                    )

        return DependencyGraph(
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            metadata={"type": "module-level"}
        )

    def _add_dependency(
        self,
        source_id: str,
        target_name: str,
        nodes: Dict[str, DependencyNode],
        edges: List[DependencyEdge],
        dep_type: str,
        language: str
    ) -> None:
        target_id = next(
            (nid for nid, n in nodes.items() if n.name == target_name),
            None
        )

        if not target_id:
            target_id = self._new_id()
            nodes[target_id] = DependencyNode(
                node_id=target_id,
                name=target_name,
                node_type="external",
                language=language
            )

        edges.append(
            DependencyEdge(
                source=source_id,
                target=target_id,
                dependency_type=dep_type
            )
        )

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Java Dependency Builder
# =========================

class JavaDependencyGraphBuilder(DependencyGraphBuilder):
    """
    Dependency graph builder for Java.
    """

    def build(self, ast_tree: ASTTree) -> DependencyGraph:
        nodes: Dict[str, DependencyNode] = {}
        edges: List[DependencyEdge] = []

        file_node_id = self._new_id()
        nodes[file_node_id] = DependencyNode(
            node_id=file_node_id,
            name=ast_tree.file_path,
            node_type="module",
            file_path=ast_tree.file_path,
            language=ast_tree.language,
        )

        def walk(node: ASTNode):
            if node.node_type == "Import":
                import_path = node.attributes.get("path")
                if import_path:
                    self._add_dependency(
                        source_id=file_node_id,
                        target_name=import_path,
                        nodes=nodes,
                        edges=edges,
                        dep_type="import",
                        language=ast_tree.language
                    )
            for child in node.children:
                walk(child)

        walk(ast_tree.root)

        return DependencyGraph(
            language=ast_tree.language,
            nodes=nodes,
            edges=edges,
            metadata={"type": "package-level"}
        )

    def _add_dependency(
        self,
        source_id: str,
        target_name: str,
        nodes: Dict[str, DependencyNode],
        edges: List[DependencyEdge],
        dep_type: str,
        language: str
    ) -> None:
        target_id = next(
            (nid for nid, n in nodes.items() if n.name == target_name),
            None
        )

        if not target_id:
            target_id = self._new_id()
            nodes[target_id] = DependencyNode(
                node_id=target_id,
                name=target_name,
                node_type="external",
                language=language
            )

        edges.append(
            DependencyEdge(
                source=source_id,
                target=target_id,
                dependency_type=dep_type
            )
        )

    @staticmethod
    def _new_id() -> str:
        return str(uuid.uuid4())


# =========================
# Builder Factory
# =========================

class DependencyGraphBuilderFactory:
    """
    Factory for selecting dependency graph builder by language.
    """

    _builders = {
        "Python": PythonDependencyGraphBuilder(),
        "Java": JavaDependencyGraphBuilder(),
    }

    @classmethod
    def get_builder(cls, language: str) -> DependencyGraphBuilder:
        if language not in cls._builders:
            raise ValueError(
                f"No dependency graph builder available for language: {language}"
            )
        return cls._builders[language]


def build_dependency_graph(ast_tree: ASTTree) -> DependencyGraph:
    """
    Functional entry point for dependency graph generation.
    """
    builder = DependencyGraphBuilderFactory.get_builder(ast_tree.language)
    return builder.build(ast_tree)
