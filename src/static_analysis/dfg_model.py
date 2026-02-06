"""
Data Flow Graph (DFG) domain models.

Purpose:
- Represent variable definitions, uses, and data dependencies
- Preserve source traceability
- Serve semantic analysis and test generation
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DFGNode:
    """
    Represents a data operation (define/use/compute).
    """
    node_id: str
    variable: Optional[str]
    operation: str  # e.g., DEFINE, USE, ASSIGN, PARAM, RETURN
    metadata: Dict[str, any] = field(default_factory=dict)


@dataclass
class DFGEdge:
    """
    Represents data dependency between operations.
    """
    source: str
    target: str
    label: Optional[str] = None  # e.g., variable name


@dataclass
class DataFlowGraph:
    """
    Container for a function or method DFG.
    """
    graph_id: str
    language: str
    nodes: Dict[str, DFGNode]
    edges: List[DFGEdge]
    metadata: Dict[str, any] = field(default_factory=dict)
