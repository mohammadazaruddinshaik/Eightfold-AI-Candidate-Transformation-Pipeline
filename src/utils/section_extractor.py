"""
Utility for extracting logical sections from resume text.
"""

from src.config.section_headers import SECTION_HEADERS


class SectionExtractor:
    """
    Extracts named sections from resume text.

    Example:
        Skills
            Python
            React

        Experience
            Google

    becomes

    {
        "skills": "Python\\nReact",
        "experience": "Google"
    }
    """

    @classmethod
    def extract(cls, text: str) -> dict[str, str]:
        """
        Extract resume sections.

        Args:
            text: Complete resume text.

        Returns:
            Dictionary mapping section names to section content.
        """

        sections: dict[str, list[str]] = {}

        current_section: str | None = None

        lines = text.splitlines()

        for raw_line in lines:

            line = raw_line.strip()

            if not line:
                continue

            matched_section = cls._match_section(line)

            if matched_section:

                current_section = matched_section

                sections.setdefault(current_section, [])

                continue

            if current_section:

                sections[current_section].append(line)

        return {
            section: "\n".join(content)
            for section, content in sections.items()
        }

    @staticmethod
    def _match_section(line: str) -> str | None:
        """
        Determine whether a line is a known section header.

        Args:
            line: Resume line.

        Returns:
            Canonical section name if matched, otherwise None.
        """

        normalized = (
            " ".join(line.lower().split())
            .rstrip(":-|")
            .strip()
        )

        for section, aliases in SECTION_HEADERS.items():

            if normalized in aliases:
                return section

        return None