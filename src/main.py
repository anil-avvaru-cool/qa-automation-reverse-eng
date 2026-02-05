
import json
from ingestion.ingestion_pipeline import run_ingestion

repository_path = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase"

result = run_ingestion(
    repo_path=repository_path,
    normalized_output_dir=f"{repository_path}/.normalized"
)

print(result["ingestion_summary"])
