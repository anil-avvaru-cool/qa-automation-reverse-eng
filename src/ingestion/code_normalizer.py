"""
Code normalizer for automation reverse engineering.

Responsibilities:
- Normalize file encoding and line endings
- Strip non-semantic noise where safe
- Produce normalized copies for downstream analysis
- Preserve original source files unmodified
"""

from pathlib import Path
from typing import Dict, List
import hashlib


class CodeNormalizer:
    """
    Normalizes source code files for reliable static analysis.
    """

    SUPPORTED_EXTENSIONS = {
        ".py", ".java", ".js", ".ts", ".rb", ".go",
        ".cs", ".cpp", ".c", ".kt", ".scala", ".sh"
    }

    def __init__(self, repo_path: str, output_dir: str | None = None):
        self.repo_path = Path(repo_path)
        self.output_dir = (
            Path(output_dir)
            if output_dir
            else self.repo_path / ".normalized"
        )

    def normalize(self) -> Dict[str, List[str]]:
        """
        Normalize source files and write them to the output directory.

        Returns:
            dict with:
              - normalized_files
              - skipped_files
        """
        normalized_files: List[str] = []
        skipped_files: List[str] = []

        for source_file in self._iter_source_files():
            try:
                normalized_path = self._normalize_file(source_file)
                normalized_files.append(str(normalized_path))
            except Exception:
                skipped_files.append(str(source_file))

        return {
            "normalized_files": normalized_files,
            "skipped_files": skipped_files
        }

    def _iter_source_files(self):
        """
        Iterate over supported source files.
        """
        ignore_dirs = {".git", ".venv", "node_modules", "__pycache__"}

        for path in self.repo_path.rglob("*"):
            if not path.is_file():
                continue

            if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
                continue

            if any(part in ignore_dirs for part in path.parts):
                continue

            yield path

    def _normalize_file(self, source_path: Path) -> Path:
        """
        Normalize a single source file.
        """
        relative_path = source_path.relative_to(self.repo_path)
        target_path = self.output_dir / relative_path

        target_path.parent.mkdir(parents=True, exist_ok=True)

        content = source_path.read_bytes()
        normalized_content = self._normalize_content(content)

        target_path.write_bytes(normalized_content)

        return target_path

    def _normalize_content(self, content: bytes) -> bytes:
        """
        Normalize content encoding and line endings.
        """
        text = content.decode("utf-8", errors="ignore")

        # Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")

        # Strip trailing whitespace
        text = "\n".join(line.rstrip() for line in text.split("\n"))

        # Ensure final newline
        if not text.endswith("\n"):
            text += "\n"

        return text.encode("utf-8")

    @staticmethod
    def compute_content_hash(content: bytes) -> str:
        """
        Compute hash for traceability and change detection.
        """
        return hashlib.sha256(content).hexdigest()


def normalize_code(repo_path: str, output_dir: str | None = None) -> Dict[str, List[str]]:
    """
    Functional entry point for code normalization.
    """
    normalizer = CodeNormalizer(repo_path, output_dir)
    return normalizer.normalize()
