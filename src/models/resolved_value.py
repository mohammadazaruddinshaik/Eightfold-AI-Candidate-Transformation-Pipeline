"""
Resolved value model.

Represents the result of conflict resolution.
"""

from typing import Any

from pydantic import BaseModel, Field

from src.models.enums import SourceType


class ResolvedValue(BaseModel):
    """
    Represents a resolved field value along with
    the source from which it was selected.
    """

    value: Any = Field(
        ...,
        description="Resolved field value."
    )

    source: SourceType = Field(
        ...,
        description="Source that contributed the resolved value."
    )