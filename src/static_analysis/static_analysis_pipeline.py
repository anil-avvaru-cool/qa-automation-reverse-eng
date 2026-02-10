"""
Static analysis pipeline for automation reverse engineering.

Responsibilities:
- Parse normalized source files into ASTs
- Build CFG, DFG, Call Graph, and Dependency Graph
- Aggregate analysis artifacts into a unified output
"""
import logging
import json
from typing import Dict, Any, List
from pydantic import BaseModel, TypeAdapter

from static_analysis.ast_model import ASTNode, ASTTree, SourceLocation
from static_analysis.cfg_model import CFGNode, CFGEdge, ControlFlowGraph
from static_analysis.dfg_model import DFGNode, DFGEdge
from static_analysis.call_graph_model import CallGraphNode, CallGraphEdge
from static_analysis.dependency_graph_model import DependencyNode, DependencyEdge, DependencyGraph
from static_analysis.ast_parser import parse_source_file
from static_analysis.cfg_builder import build_cfg
from static_analysis.dfg_builder import build_dfg
from static_analysis.call_graph_builder import build_call_graph
from static_analysis.dependency_graph_builder import build_dependency_graph


class StaticAnalysisPipeline:
    """
    Orchestrates static analysis stages.
    """
    logger = logging.getLogger(__name__)

    def __init__(self, normalized_files: List[str], language_map: Dict[str, str]):
        """
        Args:
            normalized_files: list of normalized source file paths
            language_map: mapping of file_path -> detected language
        """
        self.normalized_files = normalized_files
        self.language_map = language_map

    def run(self) -> Dict[str, Any]:
        """
        Execute static analysis pipeline.

        Returns:
            dict containing ASTs, CFGs, DFGs, call graphs, and dependency graphs
        """
        ast_trees = []
        cfgs = []
        dfgs = []
        call_graphs = []
        dependency_graphs = []

        filtered_normalized_files = [item for item in self.normalized_files if item.endswith(('OrderService.java'))]

        for file_path in filtered_normalized_files:
            language = self.language_map.get(file_path)
            if not language:
                continue

            ast_tree = parse_source_file(file_path, language)
            ast_trees.append(ast_tree)

            cfgs.extend(build_cfg(ast_tree))
            dfgs.extend(build_dfg(ast_tree))
            call_graph = build_call_graph(ast_tree)
            call_graph_json_string = call_graph.model_dump_json(indent=2)
            self.logger.info(f"Building call graph final review obj : {call_graph_json_string}")
            call_graphs.append(call_graph)
            dependency_graphs.append(build_dependency_graph(ast_tree))

        static_analysis_output = {
            "ast_trees": ast_trees,
            "control_flow_graphs": cfgs,
            "data_flow_graphs": dfgs,
            "call_graphs": call_graphs,
            "dependency_graphs": dependency_graphs,
            "analysis_summary": self._build_summary(
                ast_trees,
                cfgs,
                dfgs,
                call_graphs,
                dependency_graphs
            )
        }

        analysis_result = {
            "call_graph": [call_graph.model_dump() for call_graph in call_graphs],
            "cfgs": [cfg.model_dump() for cfg in cfgs],
            "dfgs": [dfg.model_dump() for dfg in dfgs]
        }

        self.logger.info("static_analysis_complete", analysis_result)

        
        ast_tree_adapter = TypeAdapter(List[ASTTree])        
        json_bytes = ast_tree_adapter.dump_json(ast_trees)        
        self.logger.info(f"ASTTree output:\n{json_bytes.decode()}")

        # cfg_adapter = TypeAdapter(List[ControlFlowGraph])        
        # json_bytes = cfg_adapter.dump_json(cfgs)        
        # self.logger.info(f"ControlFlowGraph output:\n{json_bytes.decode()}")

        # dfg_adapter = TypeAdapter(List[DFGNode])        
        # json_bytes = dfg_adapter.dump_json(dfgs)        
        # self.logger.info(f"DFGNode output:\n{json_bytes.decode()}")

        # call_graph_adapter = TypeAdapter(List[CallGraphNode])        
        # json_bytes = call_graph_adapter.dump_json(call_graphs)        
        # self.logger.info(f"CallGraphNode output:\n{json_bytes.decode()}")

        # dependency_graph_adapter = TypeAdapter(List[DependencyGraphNode])        
        # json_bytes = dependency_graph_adapter.dump_json(dependency_graphs)        
        # self.logger.info(f"DependencyGraphNode output:\n{json_bytes.decode()}")

        return static_analysis_output

    @staticmethod
    def _build_summary(
        asts,
        cfgs,
        dfgs,
        call_graphs,
        dependency_graphs
    ) -> Dict[str, int]:
        """
        Build a concise analysis summary.
        """
        return {
            "total_files_parsed": len(asts),
            "total_cfgs": len(cfgs),
            "total_dfgs": len(dfgs),
            "total_call_graphs nodes": len(call_graphs.nodes) if hasattr(call_graphs, 'nodes') else 0,
            "total_dependency_graphs": len(dependency_graphs)
        }


def run_static_analysis(
    normalized_files: List[str],
    language_map: Dict[str, str]
) -> Dict[str, Any]:
    """
    Functional entry point for static analysis pipeline.

    Intended usage:
    - Semantic analysis stage
    - CI/CD
    - Batch processing
    """
    pipeline = StaticAnalysisPipeline(normalized_files, language_map)
    return pipeline.run()
