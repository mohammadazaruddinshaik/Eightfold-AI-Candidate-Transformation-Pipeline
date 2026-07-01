"""
Generic conflict resolution utilities.
"""

from typing import Any

from src.models.enums import SourceType
from src.models.resolved_value import ResolvedValue


class ConflictResolver:
    """
    Resolves conflicts between values originating
    from different sources.
    """

    SOURCE_PRIORITY = [
        SourceType.RESUME,
        SourceType.CSV,
        SourceType.GITHUB,
        SourceType.LINKEDIN,
        SourceType.ATS_JSON,
        SourceType.RECRUITER_NOTES,
    ]

    @classmethod
    def resolve(
        cls,
        first_value: Any,
        second_value: Any,
        first_source: SourceType,
        second_source: SourceType,
    ) -> ResolvedValue:
        """
        Resolve conflicting values using source priority.
        """

        # Both missing
        if not first_value and not second_value:
            return ResolvedValue(
                value=None,
                source=first_source,
            )

        # Only second exists
        if not first_value:
            return ResolvedValue(
                value=second_value,
                source=second_source,
            )

        # Only first exists
        if not second_value:
            return ResolvedValue(
                value=first_value,
                source=first_source,
            )

        # Equal values
        if first_value == second_value:
            return ResolvedValue(
                value=first_value,
                source=first_source,
            )

        first_priority = cls.SOURCE_PRIORITY.index(first_source)
        second_priority = cls.SOURCE_PRIORITY.index(second_source)

        if first_priority < second_priority:
            return ResolvedValue(
                value=first_value,
                source=first_source,
            )

        return ResolvedValue(
            value=second_value,
            source=second_source,
        )