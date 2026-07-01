"""
Builds provenance information for merged candidates.
"""

from src.models.canonical_candidate import CanonicalCandidate
from src.models.enums import ProvenanceMethod
from src.models.provenance import Provenance


class ProvenanceBuilder:
    """
    Builds provenance entries for canonical candidates.
    """

    def build(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
    ) -> CanonicalCandidate:
        """
        Populate provenance for the merged candidate.
        """

        merged.provenance = {}

        self._build_field(
            merged,
            candidates,
            field="full_name",
            source_field="full_name",
            method=ProvenanceMethod.RESOLVED,
        )

        self._build_field(
            merged,
            candidates,
            field="emails",
            source_field="email",
            method=ProvenanceMethod.NORMALIZED,
        )

        self._build_field(
            merged,
            candidates,
            field="phones",
            source_field="phone",
            method=ProvenanceMethod.NORMALIZED,
        )

        
        
        self._build_field(
            merged,
            candidates,
            field="skills",
            source_field="skills",
            method=ProvenanceMethod.MERGED,
        )

        self._build_field(
            merged,
            candidates,
            field="years_experience",
            source_field="years_experience",
            method=ProvenanceMethod.RESOLVED,
        )

        self._build_location(
            merged,
            candidates,
        )
        
        self._build_links(
            merged,
            candidates,
        )
        
        self._build_experience(
            merged,
            candidates,
        )

        self._build_education(
            merged,
            candidates,
        )

        return merged



    def _build_field(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
        *,
        field: str,
        source_field: str,
        method: ProvenanceMethod,
    ) -> None:
        """
        Build provenance for a single canonical field.
        """

        merged_value = getattr(merged, field)

        if merged_value is None:
            return

        sources = []
        source_fields = []

        raw_values = []
        seen_sources = set()
        seen_fields = set()
        seen_values = set()

        for candidate in candidates:

            value = getattr(candidate, field, None)

            if value is None:
                continue

            # ----------------------------
            # List Fields
            # ----------------------------
            if isinstance(merged_value, list):

                if not value:
                    continue

                if any(item in merged_value for item in value):

                    if candidate.source not in seen_sources:
                        sources.append(candidate.source)
                        seen_sources.add(candidate.source)

                    if source_field not in seen_fields:
                        source_fields.append(source_field)
                        seen_fields.add(source_field)

                    for item in value:

                        # Handle Skill objects
                        if hasattr(item, "name"):
                            item = item.name
                        else:
                            item = str(item)

                        if item not in seen_values:
                            raw_values.append(item)
                            seen_values.add(item)

            # ----------------------------
            # Scalar Fields
            # ----------------------------
            else:

                if value == merged_value:

                    if candidate.source not in seen_sources:
                        sources.append(candidate.source)
                        seen_sources.add(candidate.source)

                    if source_field not in seen_fields:
                        source_fields.append(source_field)
                        seen_fields.add(source_field)

                    value = str(value)

                    if value not in seen_values:
                        raw_values.append(value)
                        seen_values.add(value)

        if not sources:
            return

        merged.provenance[field] = Provenance(
            field=field,
            sources=sources,
            source_fields=source_fields,
            raw_values=raw_values,
            method=method,
        )
        
        
    def _build_location(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
    ) -> None:
        """
        Build provenance for the location field.
        """

        if merged.location is None:
            return

        sources = []
        source_fields = []
        raw_values = []

        seen_sources = set()
        seen_values = set()

        for candidate in candidates:

            if candidate.location is None:
                continue

            if candidate.source not in seen_sources:
                sources.append(candidate.source)
                seen_sources.add(candidate.source)

            source_fields.append("location")

            value = ", ".join(
                filter(
                    None,
                    [
                        candidate.location.city,
                        candidate.location.region,
                        candidate.location.country,
                    ],
                )
            )

            if value not in seen_values:
                raw_values.append(value)
                seen_values.add(value)

        if not sources:
            return

        merged.provenance["location"] = Provenance(
            field="location",
            sources=sources,
            source_fields=["location"],
            raw_values=raw_values,
            method=ProvenanceMethod.RESOLVED,
        )
        
    def _build_links(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
    ) -> None:
        """
        Build provenance for candidate links.
        """

        if merged.links is None:
            return

        sources = []
        source_fields = []
        raw_values = []

        seen_sources = set()
        seen_fields = set()
        seen_values = set()

        link_fields = [
            ("linkedin", merged.links.linkedin),
            ("github", merged.links.github),
            ("portfolio", merged.links.portfolio),
        ]

        for candidate in candidates:

            if candidate.links is None:
                continue

            for field_name, merged_value in link_fields:

                if merged_value is None:
                    continue

                candidate_value = getattr(
                    candidate.links,
                    field_name,
                    None,
                )

                if candidate_value != merged_value:
                    continue

                if candidate.source not in seen_sources:
                    sources.append(candidate.source)
                    seen_sources.add(candidate.source)

                if field_name not in seen_fields:
                    source_fields.append(field_name)
                    seen_fields.add(field_name)

                if candidate_value not in seen_values:
                    raw_values.append(candidate_value)
                    seen_values.add(candidate_value)

        if not sources:
            return

        merged.provenance["links"] = Provenance(
            field="links",
            sources=sources,
            source_fields=source_fields,
            raw_values=raw_values,
            method=ProvenanceMethod.RESOLVED,
        )
        
    def _build_experience(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
    ) -> None:
        """
        Build provenance for work experience.
        """

        if not merged.experience:
            return

        sources = []
        source_fields = []
        raw_values = []

        seen_sources = set()
        seen_values = set()

        for candidate in candidates:

            if not candidate.experience:
                continue

            if candidate.source not in seen_sources:
                sources.append(candidate.source)
                seen_sources.add(candidate.source)

            for exp in candidate.experience:

                value = " | ".join(
                    filter(
                        None,
                        [
                            exp.company,
                            exp.title,
                        ],
                    )
                )

                if value and value not in seen_values:

                    raw_values.append(value)
                    seen_values.add(value)

        if not sources:
            return

        merged.provenance["experience"] = Provenance(
            field="experience",
            sources=sources,
            source_fields=["experience"],
            raw_values=raw_values,
            method=ProvenanceMethod.MERGED,
        )
        
        
    def _build_education(
        self,
        merged: CanonicalCandidate,
        candidates: list[CanonicalCandidate],
    ) -> None:
        """
        Build provenance for education.
        """

        if not merged.education:
            return

        sources = []
        source_fields = []
        raw_values = []

        seen_sources = set()
        seen_values = set()

        for candidate in candidates:

            if not candidate.education:
                continue

            if candidate.source not in seen_sources:
                sources.append(candidate.source)
                seen_sources.add(candidate.source)

            for edu in candidate.education:

                value = " | ".join(
                    filter(
                        None,
                        [
                            edu.institution,
                            edu.degree,
                        ],
                    )
                )

                if value and value not in seen_values:

                    raw_values.append(value)
                    seen_values.add(value)

        if not sources:
            return

        merged.provenance["education"] = Provenance(
            field="education",
            sources=sources,
            source_fields=["education"],
            raw_values=raw_values,
            method=ProvenanceMethod.MERGED,
        )