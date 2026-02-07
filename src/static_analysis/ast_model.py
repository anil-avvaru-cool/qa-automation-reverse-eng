"""
AST domain models for static analysis.

Purpose:
- Provide language-agnostic AST representations
- Preserve traceability to source files
- Act as a stable contract between parsing and analysis layers
"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, TypeAdapter

class SourceLocation(BaseModel):
    file_path: str
    line_start: Optional[int] = None
    line_end: Optional[int] = None
    column_start: Optional[int] = None
    column_end: Optional[int] = None

class ASTNode(BaseModel): 
    """
    Language-agnostic AST node.
    """
    node_type: str
    name: Optional[str] = None
    value: Optional[Any] = None
    children: List["ASTNode"] = Field(default_factory=list)
    location: Optional[SourceLocation] = None
    attributes: Dict[str, Any] = Field(default_factory=dict)

    def add_child(self, node: "ASTNode") -> None:
        self.children.append(node)

class ASTTree(BaseModel): 
    """
    Root container for a parsed source file.
    """
    language: str
    file_path: str
    root: ASTNode
    metadata: Dict[str, Any] = Field(default_factory=dict)
