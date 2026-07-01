"""
Identity resolution result model.
"""

from pydantic import BaseModel, Field


class IdentityMatch(BaseModel):
    """
    Represents the result of comparing two candidate profiles.
    """

    matched: bool = Field(
        ...,
        description="Whether the two candidates represent the same person."
    )

    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalized identity score between 0.0 and 1.0."
    )

    matched_on: list[str] = Field(
        default_factory=list,
        description="Fields that contributed to the identity match."
    )