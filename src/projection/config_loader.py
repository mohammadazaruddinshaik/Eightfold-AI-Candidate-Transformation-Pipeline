"""
Loads projection configurations from JSON files.
"""

import json
from pathlib import Path

from src.projection.config_models import ProjectionConfig


class ConfigLoader:
    """
    Loads runtime projection configurations.
    """

    @staticmethod
    def load(
        path: str | Path,
    ) -> ProjectionConfig:

        path = Path(path)

        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        return ProjectionConfig.model_validate(
            data,
        )