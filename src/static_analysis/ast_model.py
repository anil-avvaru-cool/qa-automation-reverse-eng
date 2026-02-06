"""
AST domain models for static analysis.

Purpose:
- Provide language-agnostic AST representations
- Preserve traceability to source files
- Act as a stable contract between parsing and analysis layers
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SourceLocation:
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    column_start: Optional[int] = None
    column_end: Optional[int] = None


@dataclass
class ASTNode:
    """
    Language-agnostic AST node.
    """
    node_type: str
    name: Optional[str] = None
    value: Optional[Any] = None
    children: List["ASTNode"] = field(default_factory=list)
    location: Optional[SourceLocation] = None
    attributes: Dict[str, Any] = field(default_factory=dict)

    def add_child(self, node: "ASTNode") -> None:
        self.children.append(node)


@dataclass
class ASTTree:
    """
    Root container for a parsed source file.
    """
    language: str
    file_path: str
    root: ASTNode
    metadata: Dict[str, Any] = field(default_factory=dict)
