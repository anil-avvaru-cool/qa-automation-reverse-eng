"""
Dependency Graph domain models.

Purpose:
- Represent structural dependencies between modules, packages, and libraries
- Support impact analysis, refactoring, and knowledge base generation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DependencyNode:
    """
    Represents a dependency unit (module, package, or external library).
    """
    node_id: str
    name: str
    node_type: str  # module, package, external
    file_path: Optional[str] = None
    language: Optional[str] = None
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass
class DependencyEdge:
    """
    Represents a dependency relationship.
    """
    source: str
    target: str
    dependency_type: str  # import, include, requires, uses


@dataclass
class DependencyGraph:
    """
    Container for the dependency graph.
    """
    language: str
    nodes: Dict[str, DependencyNode]
    edges: List[DependencyEdge]
    metadata: Dict[str, any] = field(default_factory=dict)
