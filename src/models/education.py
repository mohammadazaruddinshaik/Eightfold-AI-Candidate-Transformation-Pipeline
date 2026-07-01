"""
Education model for the canonical candidate profile.
"""

from pydantic import BaseModel, Field


class Education(BaseModel):
    """
    Represents a single education entry.
    """

    institution: str = Field(
        ...,
        description="Name of the educational institution."
    )

    degree: str | None = Field(
        default=None,
        description="Degree obtained."
    )

    field: str | None = Field(
        default=None,
        description="Field of study."
    )

    start: str | None = Field(
        default=None,
        description="Education start date."
    )

    end: str | None = Field(
        default=None,
        description="Education end date or graduation date."
    )