"""
Ingestion pipeline for automation reverse engineering system.

Responsibilities:
- Coordinate repository scanning
- Detect programming languages
- Resolve dependencies and automation frameworks
- Produce a normalized ingestion model for downstream stages
"""

from typing import Dict, Any

from ingestion.repository_scanner import scan_repository
from ingestion.language_detection import detect_languages
from ingestion.dependency_resolution import resolve_dependencies


class IngestionPipeline:
    """
    Orchestrates the ingestion phase of the system.
    """

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def run(self) -> Dict[str, Any]:
        """
        Execute the ingestion pipeline.

        Returns:
            dict with:
              - repository
              - languages
              - dependencies
              - ingestion_summary
        """
        repository_inventory = scan_repository(self.repo_path)
        language_info = detect_languages(self.repo_path)
        dependency_info = resolve_dependencies(self.repo_path)

        ingestion_output = {
            "repository": repository_inventory,
            "languages": language_info,
            "dependencies": dependency_info,
            "ingestion_summary": self._build_summary(
                repository_inventory,
                language_info,
                dependency_info
            )
        }

        return ingestion_output

    def _build_summary(
        self,
        repository: Dict[str, Any],
        languages: Dict[str, Any],
        dependencies: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Build a high-level ingestion summary for logging and reporting.
        """
        return {
            "root_path": repository.get("root_path"),
            "total_source_files": len(repository.get("source_files", [])),
            "total_config_files": len(repository.get("config_files", [])),
            "primary_language": languages.get("primary_language"),
            "detected_languages": sorted(list(languages.get("languages", []))),
            "dependency_files": dependencies.get("dependency_files", []),
            "automation_frameworks": dependencies.get("automation_frameworks", [])
        }


def run_ingestion(repo_path: str) -> Dict[str, Any]:
    """
    Functional entry point for ingestion pipeline.

    Intended usage:
        - CLI
        - CI/CD
        - Orchestration services
    """
    pipeline = IngestionPipeline(repo_path)
    return pipeline.run()
