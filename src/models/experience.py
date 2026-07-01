"""
Experience model for the canonical candidate profile.
"""

from pydantic import BaseModel, Field


class Experience(BaseModel):
    """
    Represents a single work experience entry.
    """

    company: str | None = Field(
        default=None,
        description="Company or organization name."
    )

    title: str | None = Field(
        default=None,
        description="Job title or role."
    )

    start: str | None = Field(
        default=None,
        description="Employment start date."
    )

    end: str | None = Field(
        default=None,
        description="Employment end date. None indicates current employment."
    )

    summary: str | None = Field(
        default=None,
        description="Short description of responsibilities or achievements."
    )