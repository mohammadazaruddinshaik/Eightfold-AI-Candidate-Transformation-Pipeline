"""
Parser for recruiter CSV exports.
"""

import csv
from pathlib import Path

from src.models.enums import SourceType
from src.models.experience import Experience
from src.models.raw_candidate import RawCandidate
from src.parsers.base_parser import BaseParser


class CSVParser(BaseParser):
    """
    Parses recruiter CSV exports into RawCandidate objects.
    """

    NAME_COLUMN = "name"
    EMAIL_COLUMN = "email"
    PHONE_COLUMN = "phone"
    COMPANY_COLUMN = "current_company"
    TITLE_COLUMN = "title"

    def parse(self, file_path: Path) -> RawCandidate:
        """
        Parse a recruiter CSV file into a RawCandidate.

        Args:
            file_path: Path to the recruiter CSV file.

        Returns:
            RawCandidate containing extracted candidate information.

        Raises:
            FileNotFoundError: If the CSV file does not exist.
            ValueError: If the CSV is empty.
        """

        self.ensure_file_exists(file_path)

        with file_path.open(
            mode="r",
            encoding="utf-8",
            newline=""
        ) as csv_file:

            reader = csv.DictReader(csv_file)

            try:
                row = next(reader)
            except StopIteration:
                raise ValueError("Recruiter CSV is empty.")

        experience = []

        company = row.get(self.COMPANY_COLUMN)
        title = row.get(self.TITLE_COLUMN)

        if company or title:
            experience.append(
                Experience(
                    company=company,
                    title=title
                )
            )

        return RawCandidate(
            source=SourceType.CSV,
            full_name=row.get(self.NAME_COLUMN),
            emails=self.split_values(row.get(self.EMAIL_COLUMN)),
            phones=self.split_values(row.get(self.PHONE_COLUMN)),
            experience=experience,
        )