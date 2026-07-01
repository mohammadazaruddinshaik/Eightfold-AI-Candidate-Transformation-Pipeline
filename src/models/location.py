"""
Location model for the canonical candidate profile.
"""

from pydantic import BaseModel, Field


class Location(BaseModel):
    """
    Represents a candidate's normalized location.
    """

    city: str | None = Field(
        default=None,
        description="City name."
    )

    region: str | None = Field(
        default=None,
        description="State or region."
    )

    country: str | None = Field(
        default=None,
        description="Country name."
    )