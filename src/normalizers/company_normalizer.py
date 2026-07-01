"""
Company normalization utilities.
"""

from src.normalizers.base_normalizer import BaseNormalizer


class CompanyNormalizer(BaseNormalizer):
    """
    Normalizes company names by removing common legal entity suffixes.
    """

    LEGAL_SUFFIXES = (
        " llc",
        " inc",
        " inc.",
        " ltd",
        " ltd.",
        " limited",
        " corporation",
        " corp",
        " corp.",
        " private limited",
        " pvt ltd",
    )

    @classmethod
    def normalize(cls, company: str | None) -> str | None:
        """
        Normalize a company name.

        Examples:
            Google LLC           -> Google
            Google Inc.          -> Google
            Microsoft Corp       -> Microsoft
            Eightfold AI         -> Eightfold AI
            Amazon Web Services  -> Amazon Web Services
        """

        if not company:
            return None

        company = cls.normalize_whitespace(company)

        normalized = company.lower()

        for suffix in cls.LEGAL_SUFFIXES:
            if normalized.endswith(suffix):
                company = company[:-len(suffix)].strip()
                break

        return company