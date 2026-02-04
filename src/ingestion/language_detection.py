"""
Language detection for automation codebases.

Responsibilities:
- Detect programming languages used in a repository
- Identify primary and secondary languages
- Provide file-level and repo-level language metadata
"""

from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Set


class LanguageDetector:
    """
    Detects programming languages based on file extensions
    and lightweight content heuristics.
    """

    # Canonical extension to language mapping
    EXTENSION_LANGUAGE_MAP: Dict[str, str] = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".rb": "Ruby",
        ".go": "Go",
        ".cs": "CSharp",
        ".cpp": "Cpp",
        ".c": "C",
        ".kt": "Kotlin",
        ".scala": "Scala",
        ".sh": "Shell",
        ".ps1": "PowerShell",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".json": "JSON",
        ".xml": "XML",
        ".groovy": "Groovy"
    }

    # Automation framework hints (content-based)
    FRAMEWORK_HINTS: Dict[str, Set[str]] = {
        "Python": {"selenium", "pytest", "unittest", "behave", "playwright"},
        "Java": {"selenium", "testng", "junit", "cucumber"},
        "JavaScript": {"cypress", "jest", "playwright", "webdriverio"},
        "TypeScript": {"cypress", "playwright", "jest"},
        "Ruby": {"rspec", "capybara"},
        "Shell": {"bash", "sh"},
    }

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def detect(self) -> Dict[str, object]:
        """
        Detect languages used in the repository.

        Returns:
            dict with:
              - languages: set of detected languages
              - primary_language: most dominant language
              - language_distribution: percentage per language
              - files_by_language: mapping of language -> file list
        """
        files_by_language: Dict[str, List[str]] = defaultdict(list)
        language_counter: Counter = Counter()

        for file_path in self._iter_source_files():
            language = self._detect_language_for_file(file_path)
            if not language:
                continue

            files_by_language[language].append(str(file_path))
            language_counter[language] += 1

        if not language_counter:
            return {
                "languages": set(),
                "primary_language": None,
                "language_distribution": {},
                "files_by_language": {}
            }

        total_files = sum(language_counter.values())
        distribution = {
            lang: round((count / total_files) * 100, 2)
            for lang, count in language_counter.items()
        }

        primary_language = language_counter.most_common(1)[0][0]

        return {
            "languages": set(language_counter.keys()),
            "primary_language": primary_language,
            "language_distribution": distribution,
            "files_by_language": dict(files_by_language)
        }

    def _iter_source_files(self):
        """
        Iterate through relevant source files, skipping common noise.
        """
        ignore_dirs = {".git", ".venv", "node_modules", "target", "build", "__pycache__"}

        for path in self.repo_path.rglob("*"):
            if not path.is_file():
                continue

            if any(part in ignore_dirs for part in path.parts):
                continue

            yield path

    def _detect_language_for_file(self, file_path: Path) -> str:
        """
        Detect language for a single file using extension and content.
        """
        extension = file_path.suffix.lower()

        language = self.EXTENSION_LANGUAGE_MAP.get(extension)
        if not language:
            return ""

        # Lightweight content validation for automation frameworks
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore").lower()
        except Exception:
            return language

        hints = self.FRAMEWORK_HINTS.get(language)
        if hints and any(hint in content for hint in hints):
            return language

        return language


def detect_languages(repo_path: str) -> Dict[str, object]:
    """
    Functional interface for pipeline usage.
    """
    detector = LanguageDetector(repo_path)
    return detector.detect()
