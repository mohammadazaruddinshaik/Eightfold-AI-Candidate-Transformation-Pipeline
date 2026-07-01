"""
Country normalization.
"""

import pycountry

from src.normalizers.base_normalizer import BaseNormalizer


class CountryNormalizer(BaseNormalizer):
    """
    Normalizes country names to ISO-3166 alpha-2.
    """

    @classmethod
    def normalize(cls, country: str | None) -> str | None:

        if not country:
            return None

        country = cls.normalize_whitespace(country)

        try:

            return pycountry.countries.lookup(
                country
            ).alpha_2

        except LookupError:

            return country