"""
Models representing runtime projection configuration.
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class FieldConfig(BaseModel):
    """
    Configuration for a projected field.
    """

    model_config = ConfigDict(
        populate_by_name=True,
    )

    path: str = Field(
        ...,
        description="Output field name.",
    )

    from_field: str | None = Field(
        default=None,
        alias="from",
        description="Canonical field path.",
    )

    type: str = Field(
        default="string",
    )

    required: bool = False

    normalize: str | None = None


class ProjectionConfig(BaseModel):
    """
    Runtime projection configuration.
    """

    fields: list[FieldConfig]

    include_confidence: bool = True

    include_provenance: bool = True

    on_missing: Literal[
        "null",
        "omit",
        "error",
    ] = "null"