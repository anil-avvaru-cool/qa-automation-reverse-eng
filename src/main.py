from ingestion.language_detection import detect_languages

result = detect_languages("input_codebase")

print(result["primary_language"])
print(result["language_distribution"])
