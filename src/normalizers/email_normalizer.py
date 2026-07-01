"""
Email normalization utilities.
"""

import re

from src.normalizers.base_normalizer import BaseNormalizer


class EmailNormalizer(BaseNormalizer):
    """
    Normalizes email addresses.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    @classmethod
    def normalize(cls, email: str | None) -> str | None:
        """
        Normalize an email address.

        - Removes extra whitespace.
        - Converts to lowercase.
        - Returns the original value if it is not a valid email.
        """

        if not email:
            return None

        email = cls.normalize_whitespace(email)

        if not cls.EMAIL_PATTERN.fullmatch(email):
            return email

        return email.lower()