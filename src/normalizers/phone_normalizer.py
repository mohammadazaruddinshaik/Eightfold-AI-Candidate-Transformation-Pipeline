"""
Phone number normalization.
"""

import phonenumbers

from src.normalizers.base_normalizer import BaseNormalizer


class PhoneNormalizer(BaseNormalizer):
    """
    Normalizes phone numbers to E.164 format.
    """

    DEFAULT_REGION = "IN"

    @classmethod
    def normalize(cls, phone: str | None) -> str | None:

        if not phone:
            return None

        phone = cls.normalize_whitespace(phone)

        try:
            parsed = phonenumbers.parse(
                phone,
                cls.DEFAULT_REGION,
            )

            if phonenumbers.is_valid_number(parsed):
                return phonenumbers.format_number(
                    parsed,
                    phonenumbers.PhoneNumberFormat.E164,
                )

        except phonenumbers.NumberParseException:
            pass

        return phone