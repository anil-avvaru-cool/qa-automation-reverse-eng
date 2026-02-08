"""
Dependency Graph domain models.

Purpose:
- Represent structural dependencies between modules, packages, and libraries
- Support impact analysis, refactoring, and knowledge base generation
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DependencyNode(BaseModel):
    """
    Represents a dependency unit (module, package, or external library).
    """
    node_id: str
    name: str
    node_type: str  # module, package, external
    file_path: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DependencyEdge(BaseModel):
    """
    Represents a dependency relationship.
    """
    source: str
    target: str
    dependency_type: str  # import, include, requires, uses

class DependencyGraph(BaseModel):
    """
    Container for the dependency graph.
    """
    language: str
    nodes: Dict[str, DependencyNode]
    edges: List[DependencyEdge]
    metadata: Dict[str, Any] = Field(default_factory=dict)
