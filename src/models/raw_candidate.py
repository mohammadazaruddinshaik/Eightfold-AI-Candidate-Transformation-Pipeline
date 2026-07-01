"""
Raw candidate model.

Represents candidate information extracted directly from a
single input source before normalization or merging.
"""

from pydantic import BaseModel, Field

from src.models.education import Education
from src.models.enums import SourceType
from src.models.experience import Experience
from src.models.links import Links
from src.models.location import Location


class RawCandidate(BaseModel):
    """
    Candidate information extracted from a single source.
    """

    source: SourceType

    full_name: str | None = None

    emails: list[str] = Field(default_factory=list)

    phones: list[str] = Field(default_factory=list)

    location: Location | None = None

    links: Links = Field(default_factory=Links)

    headline: str | None = None

    years_experience: float | None = None

    skills: list[str] = Field(default_factory=list)

    experience: list[Experience] = Field(default_factory=list)

    education: list[Education] = Field(default_factory=list)