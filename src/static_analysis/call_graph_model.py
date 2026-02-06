"""
Call Graph domain models.

Purpose:
- Represent inter-procedural call relationships
- Support impact analysis, entry-point discovery, and E2E test planning
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CallGraphNode:
    """
    Represents a callable unit (function or method).
    """
    node_id: str
    name: str
    file_path: str
    language: str
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass
class CallGraphEdge:
    """
    Represents a call from one function/method to another.
    """
    caller: str
    callee: str
    call_type: Optional[str] = None  # direct, virtual, static, unknown


@dataclass
class CallGraph:
    """
    Container for the complete call graph.
    """
    language: str
    nodes: Dict[str, CallGraphNode]
    edges: List[CallGraphEdge]
    entry_points: List[str] = field(default_factory=list)
    metadata: Dict[str, any] = field(default_factory=dict)
