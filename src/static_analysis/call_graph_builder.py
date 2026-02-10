from typing import Dict, List, Optional

from static_analysis.call_graph_model import (
    CallGraph,
    CallGraphNode,
    CallGraphEdge
)
from static_analysis.ast_model import ASTTree, ASTNode


def build_call_graph(ast_tree: ASTTree) -> CallGraph:
    language = ast_tree.language
    file_path = ast_tree.file_path

    nodes: Dict[str, CallGraphNode] = {}
    edges: List[CallGraphEdge] = []
    entry_points: List[str] = []

    current_class: Optional[str] = None
    current_method: Optional[str] = None

    def node_id(class_name: Optional[str], method_name: str) -> str:
        return f"{class_name}.{method_name}" if class_name else method_name

    def register_node(class_name: Optional[str], method_name: str):
        nid = node_id(class_name, method_name)
        if nid not in nodes:
            nodes[nid] = CallGraphNode(
                node_id=nid,
                name=method_name,
                file_path=file_path,
                language=language,
                metadata={
                    "class": class_name,
                    "type": "method"
                }
            )
        return nid

    def visit(node: ASTNode):
        nonlocal current_class, current_method

        node_type = node.node_type
        attributes = node.attributes or {}

        # ---------- Class ----------
        if node_type == "ClassDeclaration":
            current_class = node.name

        # ---------- Method / Constructor ----------
        elif node_type in ("MethodDeclaration", "ConstructorDeclaration"):
            current_method = register_node(current_class, node.name)

            modifiers = attributes.get("modifiers", [])
            if "public" in modifiers:
                entry_points.append(current_method)

        # ---------- Method Invocation ----------
        elif node_type == "MethodInvocation" and current_method:
            callee_method = attributes.get("member")
            qualifier = attributes.get("qualifier")

            if not callee_method:
                return

            if not qualifier:
                callee_class = current_class
                call_type = "direct"
            elif qualifier[0].isupper():
                callee_class = qualifier
                call_type = "static"
            else:
                callee_class = qualifier
                call_type = "virtual"

            callee_id = register_node(callee_class, callee_method)

            edges.append(
                CallGraphEdge(
                    caller=current_method,
                    callee=callee_id,
                    call_type=call_type
                )
            )

        # ---------- Traverse ----------
        for child in node.children or []:
            visit(child)

        # ---------- Scope reset ----------
        if node_type == "ClassDeclaration":
            current_class = None
        elif node_type in ("MethodDeclaration", "ConstructorDeclaration"):
            current_method = None

    visit(ast_tree.root)

    return CallGraph(
        language=language,
        nodes=nodes,
        edges=edges,
        entry_points=list(set(entry_points)),
        metadata={
            "builder": "call_graph_builder",
            "parser": ast_tree.metadata.get("parser")
        }
    )
