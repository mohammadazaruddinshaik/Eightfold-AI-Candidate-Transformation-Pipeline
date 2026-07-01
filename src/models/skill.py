"""
Skill model.
"""

from pydantic import BaseModel, Field

from src.models.enums import SourceType


class Skill(BaseModel):
    """
    Represents a normalized skill.
    """

    name: str = Field(
        ...,
        description="Normalized skill name.",
    )

    confidence: float = Field(
        default=1.0,
        ge=0.0,
        le=1.0,
        description="Confidence of extraction.",
    )

    sources: list[SourceType] = Field(
        default_factory=list,
        description="Sources contributing this skill.",
    )