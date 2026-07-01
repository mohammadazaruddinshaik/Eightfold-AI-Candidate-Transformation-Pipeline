"""
Candidate merger.

Merges multiple canonical candidates into a single canonical profile.
"""

import uuid

from src.merger.conflict_resolver import ConflictResolver
from src.models.canonical_candidate import CanonicalCandidate
from src.models.provenance import Provenance
from src.models.enums import ProvenanceMethod, SourceType
from src.models.skill import Skill
from src.models.enums import SourceType

class CandidateMerger:
    """
    Merges multiple canonical candidates into one canonical profile.
    """

    def merge(
        self,
        candidates: list[CanonicalCandidate],
    ) -> CanonicalCandidate:
        """
        Merge multiple canonical candidates.
        """

        if not candidates:
            raise ValueError(
                "At least one candidate is required."
            )

        merged = candidates[0]

        for candidate in candidates[1:]:

            merged = CanonicalCandidate(

                candidate_id=(
                    merged.candidate_id
                    or candidate.candidate_id
                    or str(uuid.uuid4())
                ),

                source=SourceType.CANONICAL,

                full_name=self._merge_name(
                    merged,
                    candidate,
                ),

                emails=self._merge_emails(
                    merged,
                    candidate,
                ),

                phones=self._merge_phones(
                    merged,
                    candidate,
                ),

                location=self._merge_location(
                    merged,
                    candidate,
                ),

                links=self._merge_links(
                    merged,
                    candidate,
                ),

                headline=self._merge_headline(
                    merged,
                    candidate,
                ),

                years_experience=self._merge_years_experience(
                    merged,
                    candidate,
                ),

                skills=self._merge_skills(
                    merged,
                    candidate,
                ),

                experience=self._merge_experience(
                    merged,
                    candidate,
                ),

                education=self._merge_education(
                    merged,
                    candidate,
                ),

                provenance={},

                overall_confidence=(
                    merged.overall_confidence
                    or candidate.overall_confidence
                ),
            )

        return merged

    @staticmethod
    def _merge_unique_list(
        first: list[str],
        second: list[str],
    ) -> list[str]:
        """
        Merge two lists while preserving order
        and removing duplicates.
        """

        merged = []

        for item in first + second:

            if item and item not in merged:
                merged.append(item)

        return merged
    
    
    @staticmethod
    def _is_empty(value) -> bool:
        """
        Returns True if the value should be treated as missing.
        """

        if value is None:
            return True

        if isinstance(value, str):
            return value.strip() == ""

        if isinstance(value, (list, dict)):
            return len(value) == 0

        return False


    @classmethod
    def _best_value(
        cls,
        first,
        second,
    ):
        """
        Returns the richer value.
        Empty values never win.
        """

        if cls._is_empty(first):
            return second

        if cls._is_empty(second):
            return first

        if (
            isinstance(first, str)
            and isinstance(second, str)
        ):
            return (
                first
                if len(first.strip()) >= len(second.strip())
                else second
            )

        return first

    def _merge_name(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> str | None:
        """
        Merge candidate names.
        """

        return ConflictResolver.resolve(
            first.full_name,
            second.full_name,
            first.source,
            second.source,
        ).value

    def _merge_emails(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> list[str]:
        """
        Merge email addresses.
        """

        return self._merge_unique_list(
            first.emails,
            second.emails,
        )

    def _merge_phones(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> list[str]:
        """
        Merge phone numbers.
        """

        return self._merge_unique_list(
            first.phones,
            second.phones,
        )

    def _merge_location(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ):
        """
        Merge candidate locations.
        """

        return ConflictResolver.resolve(
            first.location,
            second.location,
            first.source,
            second.source,
        ).value

    def _merge_links(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ):
        """
        Merge social/profile links.
        """

        merged = first.links.model_copy(
            deep=True
        )

        merged.linkedin = self._best_value(
            merged.linkedin,
            second.links.linkedin,
        )

        merged.github = self._best_value(
            merged.github,
            second.links.github,
        )

        merged.portfolio = self._best_value(
            merged.portfolio,
            second.links.portfolio,
        )

        merged.other = self._merge_unique_list(
            merged.other,
            second.links.other,
        )

        return merged

    def _merge_headline(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> str | None:
        """
        Merge professional headline.
        """

        return ConflictResolver.resolve(
            first.headline,
            second.headline,
            first.source,
            second.source,
        ).value

    def _merge_years_experience(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> float | None:
        """
        Merge years of experience.
        """

        if first.years_experience is None:
            return second.years_experience

        if second.years_experience is None:
            return first.years_experience

        return max(
            first.years_experience,
            second.years_experience,
        )

    def _merge_skills(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> list[Skill]:
        """
        Merge skills while tracking confidence and contributing sources.
        """

        merged: dict[str, Skill] = {}

        # -----------------------------
        # First Candidate
        # -----------------------------

        for skill in first.skills:

            if isinstance(skill, Skill):

                name = skill.name
                sources = list(skill.sources)

            else:

                name = skill
                sources = [first.source]

            merged[name.lower()] = Skill(
                name=name,
                confidence=0.90,
                sources=sources,
            )

        # -----------------------------
        # Second Candidate
        # -----------------------------

        for skill in second.skills:

            if isinstance(skill, Skill):

                name = skill.name
                sources = list(skill.sources)

            else:

                name = skill
                sources = [second.source]

            key = name.lower()

            if key in merged:

                existing = merged[key]

                existing.confidence = 1.0

                for source in sources:

                    if source not in existing.sources:
                        existing.sources.append(source)

            else:

                merged[key] = Skill(
                    name=name,
                    confidence=0.90,
                    sources=sources,
                )

        return sorted(
            merged.values(),
            key=lambda skill: skill.name.lower(),
        )
    
    
    def _merge_experience(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ):
        """
        Merge work experiences intelligently by
        deduplicating and enriching entries.
        """

        merged = list(first.experience)

        for exp in second.experience:

            matched = None

            for existing in merged:

                same_title = (
                    existing.title
                    and exp.title
                    and existing.title.lower().strip()
                    == exp.title.lower().strip()
                )

                same_company = (
                    existing.company
                    and exp.company
                    and existing.company.lower().strip()
                    == exp.company.lower().strip()
                )

                company_missing = (
                    self._is_empty(existing.company)
                    or self._is_empty(exp.company)
                )

                if same_title and (same_company or company_missing):

                    matched = existing
                    break

            if matched:

                matched.company = self._best_value(
                    matched.company,
                    exp.company,
                )

                matched.title = self._best_value(
                    matched.title,
                    exp.title,
                )

                matched.start = self._best_value(
                    matched.start,
                    exp.start,
                )

                matched.end = self._best_value(
                    matched.end,
                    exp.end,
                )

                matched.summary = self._best_value(
                    matched.summary,
                    exp.summary,
                )

            else:

                merged.append(exp)

        return merged

    def _merge_education(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ):
        """
        Merge education history.

        If an education entry already exists,
        enrich it with missing information.
        """

        merged = list(first.education)

        for edu in second.education:

            found = False

            for existing in merged:

                if (
                    existing.institution == edu.institution
                    and existing.degree == edu.degree
                ):

                    existing.field = self._best_value(
                        existing.field,
                        edu.field,
                    )

                    existing.start = self._best_value(
                        existing.start,
                        edu.start,
                    )

                    existing.end = self._best_value(
                        existing.end,
                        edu.end,
)

                    found = True
                    break

            if not found:
                merged.append(edu)

        return merged
    
    
    
    @staticmethod
    def _create_provenance(
        *,
        field: str,
        source: str,
        source_field: str,
        raw_value: str | None,
        method: ProvenanceMethod,
    ) -> Provenance:
        """
        Create a provenance entry for a canonical field.
        """

        return Provenance(
            field=field,
            source=source,
            source_field=source_field,
            raw_value=raw_value,
            method=method,
        )