"""
AST domain models for static analysis.

Purpose:
- Provide language-agnostic AST representations
- Preserve traceability to source files
- Act as a stable contract between parsing and analysis layers
"""

from __future__ import annotations
from dataclasses import dataclass, field
import uuid
from typing import Any, Dict, List, Optional, Generator
from pydantic import BaseModel, Field, TypeAdapter, PrivateAttr


class SourceLocation(BaseModel):
    start_line: Optional[int] = None
    end_line: Optional[int] = None
    start_column: Optional[int] = None
    end_column: Optional[int] = None


class ASTNode(BaseModel):
    """
    Canonical normalized AST node used across entire analysis pipeline.
    """

    # ---------------------------------------------------------
    # Identity
    # ---------------------------------------------------------

    node_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    node_type: str
    name: Optional[str] = None

    # ---------------------------------------------------------
    # Structure
    # ---------------------------------------------------------

    children: List["ASTNode"] = Field(default_factory=list)

    # ---------------------------------------------------------
    # Source Mapping
    # ---------------------------------------------------------

    location: Optional[SourceLocation] = None

    # ---------------------------------------------------------
    # Raw Parser Attributes
    # ---------------------------------------------------------

    attributes: Dict[str, Any] = Field(default_factory=dict)

    # ---------------------------------------------------------
    # Semantic Extensions (Future-Proof)
    # ---------------------------------------------------------

    modifiers: List[str] = Field(default_factory=list)
    annotations: List[str] = Field(default_factory=list)

    scope_id: Optional[str] = None        # Symbol table scope reference
    symbol_ref: Optional[str] = None     # Link to resolved symbol
    type_hint: Optional[str] = None      # Optional type info

    # ---------------------------------------------------------
    # Private Parent (Not Serialized)
    # ---------------------------------------------------------

    _parent: Optional["ASTNode"] = PrivateAttr(default=None)

    # ---------------------------------------------------------
    # Parent Handling
    # ---------------------------------------------------------

    @property
    def parent(self) -> Optional["ASTNode"]:
        return self._parent

    def set_parent(self, parent: Optional["ASTNode"]) -> None:
        self._parent = parent

    def add_child(self, child: "ASTNode") -> None:
        child.set_parent(self)
        self.children.append(child)

    # ---------------------------------------------------------
    # Traversal Utilities
    # ---------------------------------------------------------

    def walk(self) -> Generator["ASTNode", None, None]:
        yield self
        for child in self.children:
            yield from child.walk()

    def find_by_type(self, node_type: str) -> List["ASTNode"]:
        return [n for n in self.walk() if n.node_type == node_type]

    def ancestors(self) -> Generator["ASTNode", None, None]:
        current = self.parent
        while current:
            yield current
            current = current.parent

    # ---------------------------------------------------------
    # Safe Serialization
    # ---------------------------------------------------------

    def model_dump(self, *args, **kwargs):
        kwargs.setdefault("exclude", {"_parent"})
        return super().model_dump(*args, **kwargs)


ASTNode.model_rebuild()


class ASTTree(BaseModel): 
    """
    Root container for a parsed source file.
    """
    language: str
    file_path: str
    root: ASTNode
    metadata: Dict[str, Any] = Field(default_factory=dict)
