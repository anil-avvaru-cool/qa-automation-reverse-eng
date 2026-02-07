"""
Call Graph domain models.

Purpose:
- Represent inter-procedural call relationships
- Support impact analysis, entry-point discovery, and E2E test planning
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, TypeAdapter

class CallGraphNode(BaseModel):
    """
    Represents a callable unit (function or method).
    """
    node_id: str
    name: str
    file_path: str
    language: str
    metadata: Dict[str, Any] = Field(default_factory=dict)

class CallGraphEdge(BaseModel):
    """
    Represents a call from one function/method to another.
    """
    caller: str
    callee: str
    call_type: Optional[str] = None  # direct, virtual, static, unknown

class CallGraph(BaseModel):
    """
    Container for the complete call graph.
    """
    language: str
    nodes: Dict[str, CallGraphNode]
    edges: List[CallGraphEdge]
    entry_points: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
