"""
Utility for resolving nested paths from a canonical candidate.
"""

import re
from typing import Any


class PathResolver:
    """
    Resolves nested object paths.

    Examples
    --------
    full_name

    emails[0]

    links.github

    location.country

    experience[0].company
    """

    INDEX_PATTERN = re.compile(r"(.+)\[(\d+)\]")

    @classmethod
    def resolve(
        cls,
        obj: Any,
        path: str,
    ) -> Any:
        """
        Resolve a dotted path from an object.

        Returns None if any part cannot be resolved.
        """

        current = obj

        for part in path.split("."):

            if current is None:
                return None

            match = cls.INDEX_PATTERN.fullmatch(part)

            # -------------------------
            # List indexing
            # -------------------------

            if match:

                field_name = match.group(1)
                index = int(match.group(2))

                current = getattr(
                    current,
                    field_name,
                    None,
                )

                if current is None:
                    return None

                if not isinstance(current, list):
                    return None

                if index >= len(current):
                    return None

                current = current[index]

            # -------------------------
            # Normal attribute
            # -------------------------

            else:

                current = getattr(
                    current,
                    part,
                    None,
                )

        return current