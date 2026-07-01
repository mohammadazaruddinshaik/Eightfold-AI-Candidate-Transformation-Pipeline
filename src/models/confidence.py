"""
Confidence model for candidate data.
"""

from pydantic import BaseModel, Field


class Confidence(BaseModel):
    """
    Represents confidence associated with a candidate field
    or the overall candidate profile.
    """

    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0.0 and 1.0."
    )

    reason: str = Field(
        ...,
        description="Human-readable explanation for the confidence score."
    )