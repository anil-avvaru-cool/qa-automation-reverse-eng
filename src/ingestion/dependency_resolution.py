"""
Dependency resolution for automation codebases.

Responsibilities:
- Identify dependency definition files
- Parse declared dependencies per language
- Detect automation and test frameworks
- Provide normalized dependency metadata to downstream stages
"""

from pathlib import Path
from typing import Dict, List, Set
import json
import re


class DependencyResolver:
    """
    Resolves dependencies declared in common build and config files.
    """

    # Known dependency files per ecosystem
    DEPENDENCY_FILES: Set[str] = {
        "requirements.txt",
        "pyproject.toml",
        "setup.py",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts"
    }

    # Automation framework keywords
    AUTOMATION_FRAMEWORKS: Set[str] = {
        "selenium",
        "playwright",
        "cypress",
        "webdriverio",
        "pytest",
        "testng",
        "junit",
        "cucumber",
        "behave",
        "rspec",
        "capybara"
    }

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)

    def resolve(self) -> Dict[str, object]:
        """
        Resolve dependencies for the repository.

        Returns:
            dict with:
              - dependency_files
              - dependencies
              - automation_frameworks
        """
        dependencies: Set[str] = set()
        automation_frameworks: Set[str] = set()
        dependency_files: List[str] = []

        for path in self._iter_dependency_files():
            dependency_files.append(str(path.relative_to(self.repo_path)))
            parsed = self._parse_dependency_file(path)
            dependencies.update(parsed)

        for dep in dependencies:
            dep_lower = dep.lower()
            for framework in self.AUTOMATION_FRAMEWORKS:
                if framework in dep_lower:
                    automation_frameworks.add(framework)

        return {
            "dependency_files": sorted(dependency_files),
            "dependencies": sorted(dependencies),
            "automation_frameworks": sorted(automation_frameworks)
        }

    def _iter_dependency_files(self):
        """
        Locate dependency definition files in the repository.
        """
        for path in self.repo_path.rglob("*"):
            if not path.is_file():
                continue

            if path.name in self.DEPENDENCY_FILES:
                yield path

    def _parse_dependency_file(self, path: Path) -> Set[str]:
        """
        Parse a dependency file based on its type.
        """
        name = path.name

        if name == "requirements.txt":
            return self._parse_requirements_txt(path)

        if name == "package.json":
            return self._parse_package_json(path)

        if name == "pom.xml":
            return self._parse_pom_xml(path)

        if name in {"build.gradle", "build.gradle.kts"}:
            return self._parse_gradle(path)

        if name in {"pyproject.toml", "setup.py"}:
            return self._parse_python_metadata(path)

        return set()

    def _parse_requirements_txt(self, path: Path) -> Set[str]:
        deps = set()
        try:
            for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                dep = re.split(r"[<>=!]", line)[0].strip()
                deps.add(dep)
        except Exception:
            pass
        return deps

    def _parse_package_json(self, path: Path) -> Set[str]:
        deps = set()
        try:
            data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
            for section in ("dependencies", "devDependencies"):
                if section in data and isinstance(data[section], dict):
                    deps.update(data[section].keys())
        except Exception:
            pass
        return deps

    def _parse_pom_xml(self, path: Path) -> Set[str]:
        deps = set()
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r"<artifactId>(.*?)</artifactId>", content)
            deps.update(matches)
        except Exception:
            pass
        return deps

    def _parse_gradle(self, path: Path) -> Set[str]:
        deps = set()
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r"['\"]([a-zA-Z0-9_.-]+):", content)
            deps.update(matches)
        except Exception:
            pass
        return deps

    def _parse_python_metadata(self, path: Path) -> Set[str]:
        deps = set()
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
            matches = re.findall(r"['\"]([a-zA-Z0-9_.-]+)['\"]", content)
            deps.update(matches)
        except Exception:
            pass
        return deps


def resolve_dependencies(repo_path: str) -> Dict[str, object]:
    """
    Functional interface for ingestion pipeline usage.
    """
    resolver = DependencyResolver(repo_path)
    return resolver.resolve()
