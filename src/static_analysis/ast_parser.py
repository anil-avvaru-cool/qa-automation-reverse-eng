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

try:
    import javalang
except ImportError:
    javalang = None

from static_analysis.ast_model import ASTNode, ASTTree, SourceLocation


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
    language = "Java"
    logger = logging.getLogger(__name__)

    def parse(self, file_path: str) -> ASTTree:
        if javalang is None:
            raise RuntimeError(
                "javalang is required for Java parsing but is not installed"
            )

        source = Path(file_path).read_text(encoding="utf-8", errors="ignore")
        parsed = javalang.parse.parse(source)

        # for path, node in parsed.filter(javalang.tree.ClassDeclaration):
        #     self.logger.info(f"Building AST for ClassDeclaration: {node} ")

        root_node = self._convert_node(parsed, file_path)
        return ASTTree(
            language=self.language,
            file_path=file_path,
            root=root_node,
            metadata={"parser": "javalang"}
        )

    def _convert_node(
        self,
        node: Any,
        file_path: str
    ) -> ASTNode:
        node_type = type(node).__name__

        ast_node = ASTNode(
            node_type=node_type,
            name=getattr(node, "name", None),
            location=self._extract_location(node, file_path),
            attributes={}
        )

        if hasattr(node, "attrs"):
            for attr in node.attrs:
                value = getattr(node, attr)
                if isinstance(value, list):
                    for item in value:
                        if self._is_ast_node(item):
                            ast_node.add_child(
                                self._convert_node(item, file_path)
                            )
                elif self._is_ast_node(value):
                    ast_node.add_child(
                        self._convert_node(value, file_path)
                    )
                else:
                    ast_node.attributes[attr] = value

        return ast_node

    @staticmethod
    def _is_ast_node(obj: Any) -> bool:
        return hasattr(obj, "__class__") and obj.__class__.__module__.startswith(
            "javalang"
        )

    @staticmethod
    def _extract_location(
        node: Any,
        file_path: str
    ) -> Optional[SourceLocation]:
        position = getattr(node, "position", None)
        if position:
            return SourceLocation(
                file_path=file_path,
                line_start=position.line,
                column_start=position.column
            )
        return None


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
