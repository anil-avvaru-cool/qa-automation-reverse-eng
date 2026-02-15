"""
AST domain models for static analysis.

Purpose:
- Provide language-agnostic AST representations
- Preserve traceability to source files
- Act as a stable contract between parsing and analysis layers
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, TypeAdapter, PrivateAttr

class SourceLocation(BaseModel):
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    column_start: Optional[int] = None
    column_end: Optional[int] = None

class ASTNode(BaseModel):
    """
    Normalized AST node used across static analysis pipeline.

    Parent reference:
        - Stored privately
        - Excluded from serialization
        - Safe for recursive traversal
    """

    node_type: str
    name: Optional[str] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)
    children: List["ASTNode"] = Field(default_factory=list)
    line: Optional[int] = None

    # Private parent reference (NOT serialized)
    _parent: Optional["ASTNode"] = PrivateAttr(default=None)

    # ---------------------------------------------------------
    # Parent Handling
    # ---------------------------------------------------------

    @property
    def parent(self) -> Optional["ASTNode"]:
        return self._parent

    def set_parent(self, parent: Optional["ASTNode"]) -> None:
        self._parent = parent

    # ---------------------------------------------------------
    # Tree Utilities
    # ---------------------------------------------------------

    def add_child(self, child: "ASTNode") -> None:
        """
        Add child and automatically assign parent reference.
        """
        child.set_parent(self)
        self.children.append(child)

    def walk(self):
        """
        Depth-first traversal generator.
        """
        yield self
        for child in self.children:
            yield from child.walk()

    # ---------------------------------------------------------
    # Safe Serialization Override (Optional)
    # ---------------------------------------------------------

    def model_dump(self, *args, **kwargs):
        """
        Ensure parent is never serialized.
        """
        kwargs.setdefault("exclude", {"_parent"})
        return super().model_dump(*args, **kwargs)


# Required for forward references
ASTNode.model_rebuild()


class ASTTree(BaseModel): 
    """
    Root container for a parsed source file.
    """
    language: str
    file_path: str
    root: ASTNode
    metadata: Dict[str, Any] = Field(default_factory=dict)
