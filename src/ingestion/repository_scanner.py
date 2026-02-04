"""
Repository scanner for automation codebases.

Responsibilities:
- Traverse repository structure
- Collect source files and metadata
- Identify configuration and build files
- Provide normalized repository inventory for ingestion pipeline
"""

from pathlib import Path
from typing import Dict, List, Set


class RepositoryScanner:
    """
    Scans a repository and builds a structured inventory of files.
    """

    DEFAULT_IGNORE_DIRS: Set[str] = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
        "build",
        "dist",
        "target",
        ".idea",
        ".vscode"
    }

    BUILD_FILES: Set[str] = {
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Makefile"
    }

    CI_FILES: Set[str] = {
        "Jenkinsfile",
        ".gitlab-ci.yml",
        ".github"
    }

    def __init__(self, repo_path: str, ignore_dirs: Set[str] | None = None):
        self.repo_path = Path(repo_path)
        self.ignore_dirs = ignore_dirs or self.DEFAULT_IGNORE_DIRS

        if not self.repo_path.exists():
            raise FileNotFoundError(f"Repository path not found: {repo_path}")

    def scan(self) -> Dict[str, object]:
        """
        Perform repository scan.

        Returns:
            dict with:
              - root_path
              - source_files
              - config_files
              - build_files
              - ci_files
              - directory_tree
        """
        source_files: List[str] = []
        config_files: List[str] = []
        build_files: List[str] = []
        ci_files: List[str] = []

        for path in self._iter_files():
            rel_path = str(path.relative_to(self.repo_path))

            if self._is_build_file(path):
                build_files.append(rel_path)
            elif self._is_ci_file(path):
                ci_files.append(rel_path)
            elif self._is_config_file(path):
                config_files.append(rel_path)
            else:
                source_files.append(rel_path)

        return {
            "root_path": str(self.repo_path),
            "source_files": sorted(source_files),
            "config_files": sorted(config_files),
            "build_files": sorted(build_files),
            "ci_files": sorted(ci_files),
            "directory_tree": self._build_directory_tree()
        }

    def _iter_files(self):
        """
        Iterate through repository files while respecting ignore rules.
        """
        for path in self.repo_path.rglob("*"):
            if not path.is_file():
                continue

            if any(part in self.ignore_dirs for part in path.parts):
                continue

            yield path

    def _is_build_file(self, path: Path) -> bool:
        return path.name in self.BUILD_FILES

    def _is_ci_file(self, path: Path) -> bool:
        if path.name in self.CI_FILES:
            return True
        return any(ci in path.parts for ci in self.CI_FILES)

    def _is_config_file(self, path: Path) -> bool:
        return path.suffix.lower() in {".yaml", ".yml", ".json", ".ini", ".cfg", ".toml", ".xml"}

    def _build_directory_tree(self) -> Dict[str, object]:
        """
        Build a lightweight directory tree representation.
        """
        tree: Dict[str, object] = {}

        for path in self._iter_files():
            relative_parts = path.relative_to(self.repo_path).parts
            current = tree

            for part in relative_parts[:-1]:
                current = current.setdefault(part, {})

            current.setdefault("files", []).append(relative_parts[-1])

        return tree


def scan_repository(repo_path: str) -> Dict[str, object]:
    """
    Functional interface for pipeline usage.
    """
    scanner = RepositoryScanner(repo_path)
    return scanner.scan()
