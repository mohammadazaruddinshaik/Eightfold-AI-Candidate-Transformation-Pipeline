"""
Links model for the canonical candidate profile.
"""

from pydantic import BaseModel, Field


class Links(BaseModel):
    """
    Represents candidate profile links collected from different sources.
    """

    linkedin: str | None = Field(
        default=None,
        description="LinkedIn profile URL."
    )

    github: str | None = Field(
        default=None,
        description="GitHub profile URL."
    )

    portfolio: str | None = Field(
        default=None,
        description="Portfolio or personal website."
    )

    other: list[str] = Field(
        default_factory=list,
        description="Any additional relevant links."
    )