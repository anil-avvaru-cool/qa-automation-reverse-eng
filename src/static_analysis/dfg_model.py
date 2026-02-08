"""
Data Flow Graph (DFG) domain models.

Purpose:
- Represent variable definitions, uses, and data dependencies
- Preserve source traceability
- Serve semantic analysis and test generation
"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class DFGNode(BaseModel):
    """
    Represents a data operation (define/use/compute).
    """
    node_id: str
    variable: Optional[str]
    operation: str  # e.g., DEFINE, USE, ASSIGN, PARAM, RETURN
    metadata: Dict[str, Any] = Field(default_factory=dict)


class DFGEdge(BaseModel):
    """
    Represents data dependency between operations.
    """
    source: str
    target: str
    label: Optional[str] = None  # e.g., variable name


class DataFlowGraph(BaseModel):

    """
    Container for a function or method DFG.
    """
    graph_id: str
    language: str
    nodes: Dict[str, DFGNode]
    edges: List[DFGEdge]
    metadata: Dict[str, Any] = Field(default_factory=dict)