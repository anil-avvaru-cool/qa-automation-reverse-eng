"""
AST parser abstraction layer.

Purpose:
- Select language-specific AST parsers
- Produce a normalized ASTTree model
- Isolate language tooling from analysis logic
"""

from pathlib import Path
from typing import Optional, Any
import logging

import ast as python_ast

import javalang

from static_analysis.ast_model import ASTNode, ASTTree, SourceLocation

logger = logging.getLogger(__name__)

class BaseASTParser:
    """
    Base interface for language-specific AST parsers.
    """
    language: str = "unknown"

    def parse(self, file_path: str) -> ASTTree:
        raise NotImplementedError


# =========================
# Python AST Parser
# =========================

class PythonASTParser(BaseASTParser):
    language = "Python"

    def parse(self, file_path: str) -> ASTTree:
        source = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        parsed = python_ast.parse(source)

        root_node = self._convert_node(parsed, file_path)
        return ASTTree(
            language=self.language,
            file_path=file_path,
            root=root_node,
            metadata={"parser": "python_ast"}
        )

    def _convert_node(
        self,
        node: python_ast.AST,
        file_path: str
    ) -> ASTNode:
        ast_node = ASTNode(
            node_type=type(node).__name__,
            location=self._extract_location(node, file_path),
            attributes={}
        )

        for field, value in python_ast.iter_fields(node):
            if isinstance(value, python_ast.AST):
                ast_node.add_child(self._convert_node(value, file_path))
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, python_ast.AST):
                        ast_node.add_child(self._convert_node(item, file_path))
            else:
                ast_node.attributes[field] = value

        return ast_node

    @staticmethod
    def _extract_location(
        node: python_ast.AST,
        file_path: str
    ) -> Optional[SourceLocation]:
        if hasattr(node, "lineno"):
            return SourceLocation(
                file_path=file_path,
                line_start=getattr(node, "lineno", None),
                line_end=getattr(node, "end_lineno", None),
                column_start=getattr(node, "col_offset", None),
                column_end=getattr(node, "end_col_offset", None)
            )
        return None


# =========================
# Java AST Parser
# =========================
class JavaASTParser(BaseASTParser):
    """
    Java AST parser compatible with ASTParserFactory.

    Contract:
        parse(file_path: str) -> ASTTree
    """

    language = "java"

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def parse(self, file_path: str) -> ASTTree:
        """
        Parse Java file and return normalized ASTTree.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()
        except Exception:
            logger.exception(
                "Failed to read Java file",
                extra={"file_path": file_path}
            )
            raise

        try:
            raw_tree = javalang.parse.parse(source_code)
        except Exception:
            logger.exception(
                "Java parsing failed",
                extra={"file_path": file_path}
            )
            raise

        normalized_root = self._normalize_node(
            raw_tree,
            parent=None
        )

        logger.info(
            "Java AST parsing and normalization complete",
            extra={"file_path": file_path}
        )

        return ASTTree(
            language=self.language,
            file_path=file_path,
            root=normalized_root
        )

    # ---------------------------------------------------------
    # Recursive Normalization (Parent-Safe)
    # ---------------------------------------------------------

    def _normalize_node(
        self,
        node: Any,
        parent: Optional[ASTNode]
    ) -> Optional[ASTNode]:

        if node is None:
            return None

        if isinstance(node, (str, int, float, bool)):
            return None

        if not isinstance(node, javalang.ast.Node):
            return None

        node_type = type(node).__name__
        name = getattr(node, "name", None)

        line = None
        if hasattr(node, "position") and node.position:
            line = node.position.line

        attributes = {}

        for attr in node.attrs:
            value = getattr(node, attr)

            if isinstance(value, (str, int, float, bool)):
                attributes[attr] = value
            elif isinstance(value, list):
                continue
            elif isinstance(value, javalang.ast.Node):
                continue
            else:
                attributes[attr] = str(value)

        normalized = ASTNode(
            node_type=node_type,
            name=name,
            attributes=attributes,
            line=line
        )

        if parent:
            normalized.set_parent(parent)

        for child in node.children:
            if isinstance(child, list):
                for sub_child in child:
                    child_node = self._normalize_node(
                        sub_child,
                        normalized
                    )
                    if child_node:
                        normalized.add_child(child_node)
            else:
                child_node = self._normalize_node(
                    child,
                    normalized
                )
                if child_node:
                    normalized.add_child(child_node)

        return normalized


# =========================
# Parser Factory
# =========================

class ASTParserFactory:
    """
    Factory for selecting AST parser by language.
    """

    _parsers = {
        "Python": PythonASTParser(),
        "Java": JavaASTParser()
    }

    @classmethod
    def get_parser(cls, language: str) -> BaseASTParser:
        if language not in cls._parsers:
            raise ValueError(f"No AST parser available for language: {language}")
        return cls._parsers[language]


def parse_source_file(file_path: str, language: str) -> ASTTree:
    """
    Functional entry point for AST parsing.
    """
    parser = ASTParserFactory.get_parser(language)
    return parser.parse(file_path)
