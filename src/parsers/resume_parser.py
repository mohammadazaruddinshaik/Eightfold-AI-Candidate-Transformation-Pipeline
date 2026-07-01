"""
Resume PDF parser.
"""

import re
from pathlib import Path

import fitz

from src.models.location import Location
from src.models.experience import Experience
from src.config.section_headers import SECTION_HEADERS
from src.parsers.base_parser import BaseParser
from src.models.links import Links
from src.models.raw_candidate import RawCandidate
from src.models.education import Education
from src.models.enums import SourceType
from src.utils.section_extractor import SectionExtractor
from src.config.patterns import (
    EMAIL_PATTERN,
    PHONE_PATTERN,
    LINKEDIN_PATTERN,
    GITHUB_PATTERN,
    PORTFOLIO_PATTERN,
)


class ResumeParser(BaseParser):
    """
    Parses a resume PDF into a RawCandidate.
    """

    def parse(self, file_path: Path) -> RawCandidate:

        text = self._extract_text(file_path)

        sections = SectionExtractor.extract(text)

        return RawCandidate(
            source=SourceType.RESUME,

            full_name=self._extract_name(text),

            emails=self._extract_emails(text),

            phones=self._extract_phones(text),

            links=self._extract_links(text),

            headline=self._extract_headline(text),

            skills=self._extract_skills(sections),

            years_experience=self._extract_years_experience(sections),

            experience=self._extract_experience(sections),

            location=self._extract_location(text),

            education=self._extract_education(sections),
        )
    
    
    @staticmethod
    def _extract_text(file_path: Path) -> str:
        """
        Extract text from a PDF resume.
        """

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text
    
    
    @staticmethod
    def _extract_emails(text: str) -> list[str]:

        return list(
            dict.fromkeys(
                re.findall(
                    EMAIL_PATTERN,
                    text,
                    flags=re.IGNORECASE,
                )
            )
        )
        
        
    @staticmethod
    def _extract_phones(text: str) -> list[str]:

        phones = re.findall(
            PHONE_PATTERN,
            text,
        )

        return list(
            dict.fromkeys(
                phone.strip()
                for phone in phones
                if phone.strip()
            )
        )
    
    
    @staticmethod
    def _extract_links(text: str) -> Links:
        """
        Extract known profile links from the resume.
        """

        linkedin = re.search(
            LINKEDIN_PATTERN,
            text,
            re.IGNORECASE,
        )

        github = re.search(
            GITHUB_PATTERN,
            text,
            re.IGNORECASE,
        )

        return Links(
            linkedin=ResumeParser._normalize_url(
                linkedin.group(0)
            ) if linkedin else None,

            github=ResumeParser._normalize_url(
                github.group(0)
            ) if github else None,

            portfolio=None,

            other=[],
        )
    
    
    @staticmethod
    def _normalize_url(url: str) -> str:
        """
        Ensure URLs include a scheme.
        """

        if not url.startswith(("http://", "https://")):
            return f"https://{url}"

        return url
    
    @staticmethod
    def _extract_name(text: str) -> str | None:
        """
        Extract candidate name from the top of the resume.

        Heuristic:
        - Scan lines from the top.
        - Ignore emails, phones, URLs and section headers.
        - Return the first remaining line.
        """

        lines = text.splitlines()

        section_headers = {
            alias
            for aliases in SECTION_HEADERS.values()
            for alias in aliases
        }

        for raw_line in lines:

            line = raw_line.strip()

            if not line:
                continue

            normalized = (
                " ".join(line.lower().split())
                .rstrip(":-|")
                .strip()
            )

            # Skip section headers
            if normalized in section_headers:
                continue

            # Skip email
            if re.search(EMAIL_PATTERN, line, re.IGNORECASE):
                continue

            # Skip phone
            if re.search(PHONE_PATTERN, line):
                continue

            # Skip LinkedIn
            if re.search(LINKEDIN_PATTERN, line, re.IGNORECASE):
                continue

            # Skip GitHub
            if re.search(GITHUB_PATTERN, line, re.IGNORECASE):
                continue

            return line

        return None
    
    
    @staticmethod
    def _extract_skills(
        sections: dict[str, str],
    ) -> list[str]:
        """
        Extract skills from the skills section.

        Supports formats like:

        Languages: Java, Python
        Frameworks: React, FastAPI
        Tools: Git, Docker
        """

        skills_section = sections.get("skills")

        if not skills_section:
            return []

        skills = []
        seen = set()

        for line in skills_section.splitlines():

            line = line.strip()

            if not line:
                continue

            # Remove category labels like:
            # Languages:
            # Frameworks:
            if ":" in line:
                _, line = line.split(":", 1)

            for skill in line.split(","):

                skill = skill.strip()

                if skill and skill not in seen:
                    seen.add(skill)
                    skills.append(skill)

        return skills
    
    
    
    @staticmethod
    def _extract_education(
        sections: dict[str, str],
    ) -> list[Education]:
        """
        Extract education information from the education section.

        Assumptions:
        - First line: Institution
        - Second line: Degree
        - One line contains the date range
        """

        education_text = sections.get("education")

        if not education_text:
            return []

        lines = [
            line.strip()
            for line in education_text.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            return []

        institution = lines[0]

        degree = lines[1]

        # Remove CGPA if present
        if ", CGPA:" in degree:
            degree = degree.split(", CGPA:", 1)[0].strip()

        start = None
        end = None

        for line in lines:

            if "–" in line or "-" in line:

                separator = "–" if "–" in line else "-"

                parts = [
                    part.strip()
                    for part in line.split(separator, 1)
                ]

                if len(parts) == 2:
                    start = parts[0]
                    end = parts[1]

                break

        return [
            Education(
                institution=institution,
                degree=degree,
                start=start,
                end=end,
            )
        ]
        
    @staticmethod
    def _extract_headline(text: str) -> str | None:
        """
        Extract professional headline if explicitly present.
        """

        return None



    @staticmethod
    def _extract_location(text: str) -> Location | None:
        """
        Extract candidate location.

        Heuristic:
        Uses the line immediately after the candidate name.
        """

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        if len(lines) < 2:
            return None

        location = lines[1]

        if "|" in location:
            location = location.split("|")[0].strip()

        parts = [part.strip() for part in location.split(",")]

        city = parts[0] if len(parts) > 0 else None
        region = parts[1] if len(parts) > 1 else None
        country = parts[2] if len(parts) > 2 else None

        return Location(
            city=city,
            region=region,
            country=country,
        )
        
    
    @staticmethod
    def _extract_years_experience(
        sections: dict[str, str],
    ) -> float | None:
        """
        Estimate total years of experience from the experience section.
        """

        experience_text = sections.get("experience")

        if not experience_text:
            return None

        total_months = 0

        pattern = (
            r"([A-Za-z]{3})\s+(\d{4})\s*[–-]\s*"
            r"(Present|[A-Za-z]{3}\s+\d{4})"
        )

        month_map = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        from datetime import datetime

        current = datetime.now()

        for match in re.finditer(pattern, experience_text):

            start_month, start_year, end = match.groups()

            start = datetime(
                int(start_year),
                month_map[start_month],
                1,
            )

            if end == "Present":
                finish = current
            else:
                month, year = end.split()
                finish = datetime(
                    int(year),
                    month_map[month],
                    1,
                )

            months = (
                (finish.year - start.year) * 12
                + finish.month
                - start.month
            )

            total_months += max(months, 0)

        return max(
            round(total_months / 12, 1),
            0.1
        )



    @staticmethod
    def _extract_experience(
        sections: dict[str, str],
    ) -> list[Experience]:
        """
        Extract work experience from the experience section.

        Expected format:

        Role, Company
        Sep 2025 – Nov 2025

        • Responsibility
        • Responsibility
        """

        experience_text = sections.get("experience")

        if not experience_text:
            return []

        lines = [
            line.strip()
            for line in experience_text.splitlines()
            if line.strip()
        ]

        experiences = []

        i = 0

        date_pattern = (
            r"([A-Za-z]{3}\s+\d{4})\s*[–-]\s*"
            r"(Present|[A-Za-z]{3}\s+\d{4})"
        )

        while i < len(lines):

            role_company = lines[i]

            if (
                i + 1 < len(lines)
                and re.fullmatch(date_pattern, lines[i + 1])
            ):

                date_line = lines[i + 1]

                start, end = re.fullmatch(
                    date_pattern,
                    date_line,
                ).groups()

                if "," in role_company:

                    title, company = [
                        value.strip()
                        for value in role_company.split(",", 1)
                    ]

                else:

                    title = role_company
                    company = None

                i += 2

                summary = []

                while (
                    i < len(lines)
                    and not re.fullmatch(date_pattern, lines[i])
                ):

                    # Next experience starts
                    if (
                        i + 1 < len(lines)
                        and re.fullmatch(
                            date_pattern,
                            lines[i + 1],
                        )
                    ):
                        break

                    summary.append(
                        lines[i].lstrip("•").strip()
                    )

                    i += 1

                experiences.append(

                    Experience(
                        company=company,
                        title=title,
                        start=start,
                        end=end,
                        summary="\n".join(summary),
                    )

                )

            else:

                i += 1

        return experiences