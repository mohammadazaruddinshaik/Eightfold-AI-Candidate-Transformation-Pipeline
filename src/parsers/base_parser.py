"""
Base parser containing common utility methods shared by all parsers.
"""

from pathlib import Path


class BaseParser:
    """
    Base parser with reusable helper methods.
    """

    @staticmethod
    def ensure_file_exists(file_path: Path) -> None:
        """
        Raises FileNotFoundError if the file does not exist.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def clean_text(text: str | None) -> str:
        """
        Removes extra whitespace and normalizes spacing.
        """
        if not text:
            return ""

        return " ".join(text.split())

    @staticmethod
    def split_values(value: str | None, delimiter: str = ",") -> list[str]:
        """
        Splits a delimited string into a clean list.
        """

        if not value:
            return []

        return [
            item.strip()
            for item in value.split(delimiter)
            if item.strip()
        ]