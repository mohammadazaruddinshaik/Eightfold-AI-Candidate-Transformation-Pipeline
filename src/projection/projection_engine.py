"""
Runtime configurable projection engine.
"""

from pydantic import BaseModel

from src.models.canonical_candidate import CanonicalCandidate
from src.projection.config_models import ProjectionConfig
from src.projection.path_resolver import PathResolver


class ProjectionEngine:
    """
    Projects a canonical candidate into a configurable output.
    """

    def project(
        self,
        candidate: CanonicalCandidate,
        config: ProjectionConfig,
    ) -> dict:
        """
        Project the canonical candidate according to the
        supplied runtime configuration.
        """

        output = {}

        # --------------------------------------------------
        # Project Configured Fields
        # --------------------------------------------------

        for field in config.fields:

            source_path = field.from_field or field.path

            value = PathResolver.resolve(
                candidate,
                source_path,
            )

            # --------------------------------------------------
            # Handle Missing Values
            # --------------------------------------------------

            if value is None:

                if config.on_missing == "omit":
                    continue

                if config.on_missing == "error":
                    raise ValueError(
                        f"Missing required field: {source_path}"
                    )

                output[field.path] = None
                continue

            # --------------------------------------------------
            # Convert Pydantic Models
            # --------------------------------------------------

            if isinstance(value, BaseModel):

                output[field.path] = value.model_dump()

            # --------------------------------------------------
            # Convert List of Pydantic Models
            # --------------------------------------------------

            elif (
                isinstance(value, list)
                and value
                and all(
                    isinstance(item, BaseModel)
                    for item in value
                )
            ):

                output[field.path] = [
                    item.model_dump()
                    for item in value
                ]

            # --------------------------------------------------
            # Primitive Values / Lists
            # --------------------------------------------------

            else:

                output[field.path] = value

        # --------------------------------------------------
        # Overall Confidence
        # --------------------------------------------------

        if config.include_confidence:

            output["overall_confidence"] = (
                candidate.overall_confidence.model_dump()
                if candidate.overall_confidence
                else None
            )

        # --------------------------------------------------
        # Provenance
        # --------------------------------------------------

        if config.include_provenance:

            output["provenance"] = {
                field: provenance.model_dump()
                for field, provenance in candidate.provenance.items()
            }

        return output