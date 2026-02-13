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
    node_id: str
    variable_name: str
    kind: str  # definition | usage | parameter | return
    method_id: str
    line: Optional[int] = None


class DFGEdge(BaseModel):
    edge_id: str
    source_node_id: str
    target_node_id: str
    relation: str  # flows_to


class DataFlowGraph(BaseModel):
    graph_id: str
    language: str
    method_id: str
    nodes: List[DFGNode] = Field(default_factory=list)
    edges: List[DFGEdge] = Field(default_factory=list)
    metadata: Dict[str, str] = Field(default_factory=dict)
