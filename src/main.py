
import json
from ingestion.ingestion_pipeline import run_ingestion

repository_path = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase"
result = run_ingestion(repository_path)
print(result["ingestion_summary"])
#print(result)
# formatted_json = json.dumps(list(result), indent=4)
# print("Formatted JSON output:")
# print(formatted_json)




# from ingestion.language_detection import detect_languages
# from ingestion.repository_scanner import scan_repository
# from ingestion.dependency_resolution import resolve_dependencies

# repository_path = "/home/vboxuser/src/qa-automation-reverse-eng/src/input_codebase"

# deps = resolve_dependencies(repository_path)

# print("Automation frameworks:", deps["automation_frameworks"])
# print("Dependencies:", deps["dependencies"])

# inventory = scan_repository(repository_path)

# print("build_files:", inventory["build_files"])
# print("ci_files:", inventory["ci_files"])
# print("source_files count:", len(inventory["source_files"]))


# result = detect_languages(repository_path)

# print(result["primary_language"])
# print(result["language_distribution"])
# #print(result["files_by_language"])
# #print(result["languages"])

