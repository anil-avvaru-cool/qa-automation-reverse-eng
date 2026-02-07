"""
Language detection for automation reverse engineering.

Responsibilities:
- Detect programming languages per file
- Produce file-level language mapping
- Emit normalized file language mapping for static analysis
"""

from pathlib import Path
from typing import Dict, Set
import pprint
import logging
import json

logger = logging.getLogger(__name__)

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".java": "Java",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".rb": "Ruby",
    ".go": "Go",
    ".cs": "CSharp",
    ".cpp": "CPP",
    ".c": "C",
    ".kt": "Kotlin",
    ".scala": "Scala",
    ".sh": "Shell",
}


def detect_languages(
    repo_path: str,
    normalized_root: str | None = None
) -> Dict[str, object]:
    """
    Detect languages used in a repository.

    Args:
        repo_path: root of the original repository
        normalized_root: root directory of normalized sources

    Returns:
        dict containing:
          - primary_language
          - languages
          - file_language_map
          - file_language_map_normalized
    """
    repo_root = Path(repo_path)
    normalized_root_path = (
        Path(normalized_root)
        if normalized_root
        else repo_root / ".normalized"
    )

    file_language_map: Dict[str, str] = {}
    file_language_map_normalized: Dict[str, str] = {}
    languages: Set[str] = set()

    ignore_dirs = {".git", ".venv", "node_modules", "__pycache__"}

    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in ignore_dirs for part in path.parts):
            continue

        language = EXTENSION_LANGUAGE_MAP.get(path.suffix.lower())
        if not language:
            continue

        original_path = str(path)
        normalized_path = str(
            normalized_root_path / path.relative_to(repo_root)
        )

        file_language_map[original_path] = language
        file_language_map_normalized[normalized_path] = language
        languages.add(language)

    primary_language = (
        max(languages, key=lambda lang: list(file_language_map.values()).count(lang))
        if languages
        else None
    )

    result_dict = {
        "primary_language": primary_language,
        "languages": sorted(languages),
        "file_language_map": file_language_map,
        "file_language_map_normalized": file_language_map_normalized
    }
    
    # formatted_json_string = json.dumps(result_dict, indent=4, sort_keys=True)    
    # logger.info(f"language detection result_dict:\n{formatted_json_string}")

    return result_dict
