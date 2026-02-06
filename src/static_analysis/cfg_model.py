"""
Control Flow Graph (CFG) domain models.

Purpose:
- Represent executable control flow
- Preserve source traceability
- Serve as input to semantic and test-generation layers
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class CFGNode:
    """
    Represents a basic block or control point.
    """
    node_id: str
    node_type: str
    label: Optional[str] = None
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass
class CFGEdge:
    """
    Represents a directed control-flow transition.
    """
    source: str
    target: str
    condition: Optional[str] = None


@dataclass
class ControlFlowGraph:
    """
    Container for a function or method CFG.
    """
    graph_id: str
    language: str
    entry_node: str
    exit_nodes: List[str]
    nodes: Dict[str, CFGNode]
    edges: List[CFGEdge]
    metadata: Dict[str, any] = field(default_factory=dict)
