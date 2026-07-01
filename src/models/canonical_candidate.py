"""
Canonical candidate model.

Represents the unified candidate profile after normalization,
identity resolution, and conflict resolution.
"""

from pydantic import BaseModel, Field

from src.models.confidence import Confidence
from src.models.education import Education
from src.models.enums import SourceType
from src.models.experience import Experience
from src.models.links import Links
from src.models.location import Location
from src.models.provenance import Provenance
from src.models.skill import Skill


class CanonicalCandidate(BaseModel):
    """
    Canonical representation of a candidate.
    """

    candidate_id: str | None = Field(
        default=None,
        description="Unique candidate identifier generated after identity resolution."
    )

    source: SourceType = Field(
        ...,
        description="Source from which this canonical profile was created."
    )

    full_name: str | None = Field(
        default=None,
        description="Candidate's full name."
    )

    emails: list[str] = Field(
        default_factory=list,
        description="Normalized email addresses."
    )

    phones: list[str] = Field(
        default_factory=list,
        description="Normalized phone numbers."
    )

    location: Location | None = Field(
        default=None,
        description="Normalized candidate location."
    )

    links: Links = Field(
        default_factory=Links,
        description="Candidate profile links."
    )

    headline: str | None = Field(
        default=None,
        description="Professional headline."
    )

    years_experience: float | None = Field(
        default=None,
        description="Total years of professional experience."
    )

    skills: list[Skill] = Field(
        default_factory=list,
        description="Normalized skills."
    )

    experience: list[Experience] = Field(
        default_factory=list,
        description="Employment history."
    )

    education: list[Education] = Field(
        default_factory=list,
        description="Educational qualifications."
    )

    provenance: dict[str, Provenance] = Field(
        default_factory=dict,
        description="Field-level provenance."
    )

    overall_confidence: Confidence | None = Field(
        default=None,
        description="Overall confidence assigned after merging and conflict resolution."
    )