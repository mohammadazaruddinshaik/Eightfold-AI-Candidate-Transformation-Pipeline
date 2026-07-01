"""
Base normalizer containing reusable helper methods.
"""

class BaseNormalizer:
    """
    Base class for all normalizers.
    """

    @staticmethod
    def normalize_whitespace(value: str | None) -> str | None:
        """
        Remove extra whitespace from a string.
        """
        if value is None:
            return None

        return " ".join(value.split())

    @staticmethod
    def normalize_case(value: str | None) -> str | None:
        """
        Trim leading/trailing whitespace.
        """
        if value is None:
            return None

        return value.strip()