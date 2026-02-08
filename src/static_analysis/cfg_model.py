"""
Control Flow Graph (CFG) domain models.

Purpose:
- Represent executable control flow
- Preserve source traceability
- Serve as input to semantic and test-generation layers
"""


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field

class CFGNode(BaseModel):
    """
    Represents a basic block or control point.
    """
    node_id: str
    node_type: str
    label: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class CFGEdge(BaseModel):
    """
    Represents a directed control-flow transition.
    """
    source: str
    target: str
    condition: Optional[str] = None


class ControlFlowGraph(BaseModel):
    """
    Container for a function or method CFG.
    """
    graph_id: str
    language: str
    entry_node: str
    exit_nodes: List[str]
    nodes: Dict[str, CFGNode]
    edges: List[CFGEdge]
    metadata: Dict[str, Any] = Field(default_factory=dict)
