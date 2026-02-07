import logging
import json
from ingestion.ingestion_pipeline import run_ingestion
from static_analysis.static_analysis_pipeline import run_static_analysis

import shutil
import os

logging.basicConfig(
    level=logging.DEBUG,  # Lowest level to capture
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler("app.log"),      # Logs everything to a file
        # logging.StreamHandler()             # Also prints to the console
    ]
)

repository_path = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase"
#file_path_ast = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase/.normalized/Selenium_framework-BDD-Cucumber/src/test/java/modules/Web/OrderSummaryPage.java"
output_directory_path = f"{repository_path}/.normalized"
try:
    shutil.rmtree(output_directory_path)
    print(f"Directory '{output_directory_path}' and all its contents have been removed.")
except FileNotFoundError:
    print(f"Error: The directory '{output_directory_path}' was not found.")
except OSError as e:
    print(f"Error deleting directory '{output_directory_path}': {e}")

ingestion_result = run_ingestion(
    repo_path=repository_path,
    normalized_output_dir=output_directory_path
)

analysis_output = run_static_analysis(
    normalized_files=ingestion_result["normalization"]["normalized_files"],
    language_map = ingestion_result["languages"]["file_language_map_normalized"]
)
print(analysis_output["analysis_summary"])
