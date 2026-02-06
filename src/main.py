
import json
from ingestion.ingestion_pipeline import run_ingestion
from static_analysis.ast_parser import parse_source_file
from static_analysis.cfg_builder import build_cfg

file_path_ast = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/test/java/modules/Web/OrderSummaryPage.java"
ast_result = parse_source_file(file_path_ast, "Java")
# print("ast_result: ",ast_result)

cfgs = build_cfg(ast_result)
print("cfgs: ", cfgs)

# repository_path = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase"

# result = run_ingestion(
#     repo_path=repository_path,
#     normalized_output_dir=f"{repository_path}/.normalized"
# )

# print(result["ingestion_summary"])
