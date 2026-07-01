"""
Provenance model for tracking the origin of canonical candidate fields.
"""

from pydantic import BaseModel, Field

from src.models.enums import (
    ProvenanceMethod,
    SourceType,
)


class Provenance(BaseModel):
    """
    Describes how a canonical field was produced.
    """

    field: str = Field(
        ...,
        description="Canonical field name.",
    )

    sources: list[SourceType] = Field(
        default_factory=list,
        description="Sources contributing to this field.",
    )

    source_fields: list[str] = Field(
        default_factory=list,
        description="Original source field names.",
    )

    raw_values: list[str] = Field(
        default_factory=list,
        description="Original values before normalization.",
    )

    method: ProvenanceMethod = Field(
        ...,
        description="How the value was obtained.",
    )