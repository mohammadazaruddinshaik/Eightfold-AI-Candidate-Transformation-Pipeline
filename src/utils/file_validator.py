"""
Utility functions for validating input and output paths.
"""

from pathlib import Path


class FileValidator:
    """
    Validates CLI input files.
    """

    @staticmethod
    def validate_file(path: Path, name: str) -> None:
        """
        Ensure a file exists.
        """

        if not path.exists():
            raise FileNotFoundError(
                f"{name} not found: {path}"
            )

        if not path.is_file():
            raise ValueError(
                f"{name} is not a file: {path}"
            )

    @staticmethod
    def prepare_output(path: Path) -> None:
        """
        Create output directory if needed.
        """

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )