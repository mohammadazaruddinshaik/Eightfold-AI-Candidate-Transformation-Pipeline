"""
Validation result model.
"""

from pydantic import BaseModel, Field


class ValidationResult(BaseModel):
    """
    Represents projection validation result.
    """

    valid: bool = Field(
        ...,
        description="Whether projection is valid.",
    )

    errors: list[str] = Field(
        default_factory=list,
        description="Validation errors.",
    )

    warnings: list[str] = Field(
        default_factory=list,
        description="Validation warnings.",
    )