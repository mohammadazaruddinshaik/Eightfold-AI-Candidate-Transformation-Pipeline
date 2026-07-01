"""
Validates projected output against runtime configuration.
"""

import re

from src.projection.config_models import ProjectionConfig
from src.validation.validation_result import ValidationResult


class ProjectionValidator:
    """
    Validates projected output.
    """

    EMAIL_PATTERN = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    PHONE_PATTERN = re.compile(
        r"^\+[1-9]\d{7,14}$"
    )

    DATE_PATTERN = re.compile(
        r"^\d{4}-\d{2}$"
    )

    URL_PATTERN = re.compile(
        r"^https?://"
    )

    def validate(
        self,
        projection: dict,
        config: ProjectionConfig,
    ) -> ValidationResult:

        errors = []
        warnings = []

        for field in config.fields:

            value = projection.get(field.path)

            # ----------------------------------
            # Required Validation
            # ----------------------------------

            if field.required:

                if value is None:

                    errors.append(
                        f"Required field '{field.path}' is missing."
                    )

                    continue

                if (
                    isinstance(value, str)
                    and not value.strip()
                ):

                    errors.append(
                        f"Required field '{field.path}' cannot be empty."
                    )

                    continue

            if value is None:
                continue

            # ----------------------------------
            # Type Validation
            # ----------------------------------

            if field.type == "string":

                if not isinstance(value, str):

                    errors.append(
                        f"'{field.path}' should be string."
                    )

                    continue

            elif field.type == "number":

                if not isinstance(
                    value,
                    (
                        int,
                        float,
                    ),
                ):

                    errors.append(
                        f"'{field.path}' should be number."
                    )

                    continue

            elif field.type == "array":

                if not isinstance(
                    value,
                    list,
                ):

                    errors.append(
                        f"'{field.path}' should be array."
                    )

                    continue

            elif field.type == "object":

                if not isinstance(
                    value,
                    dict,
                ):

                    errors.append(
                        f"'{field.path}' should be object."
                    )

                    continue

            # ----------------------------------
            # Format Validation
            # ----------------------------------

            normalize = field.normalize

            if (
                normalize == "email"
                and isinstance(value, str)
            ):

                if not self.EMAIL_PATTERN.match(value):

                    errors.append(
                        f"'{field.path}' is not a valid email."
                    )

            elif (
                normalize == "phone"
                and isinstance(value, str)
            ):

                if not self.PHONE_PATTERN.match(value):

                    errors.append(
                        f"'{field.path}' is not a valid E.164 phone number."
                    )

            elif (
                normalize == "date"
                and isinstance(value, str)
            ):

                if (
                    value != "Present"
                    and not self.DATE_PATTERN.match(value)
                ):

                    errors.append(
                        f"'{field.path}' should be YYYY-MM."
                    )

            elif (
                normalize == "url"
                and isinstance(value, str)
            ):

                if not self.URL_PATTERN.match(value):

                    errors.append(
                        f"'{field.path}' is not a valid URL."
                    )

        # ----------------------------------
        # Overall Confidence
        # ----------------------------------

        confidence = projection.get(
            "overall_confidence"
        )

        if confidence is not None:

            if not isinstance(
                confidence,
                dict,
            ):

                errors.append(
                    "'overall_confidence' should be object."
                )

            else:

                score = confidence.get("score")

                if (
                    not isinstance(
                        score,
                        (
                            int,
                            float,
                        ),
                    )
                    or score < 0
                    or score > 1
                ):

                    errors.append(
                        "'overall_confidence.score' must be between 0 and 1."
                    )

        # ----------------------------------
        # Skills Validation
        # ----------------------------------

        skills = projection.get("skills")

        if skills is not None:

            if not isinstance(
                skills,
                list,
            ):

                errors.append(
                    "'skills' should be array."
                )

            else:

                for index, skill in enumerate(skills):

                    if not isinstance(
                        skill,
                        dict,
                    ):

                        errors.append(
                            f"Skill[{index}] should be object."
                        )

                        continue

                    if not skill.get("name"):

                        errors.append(
                            f"Skill[{index}] missing name."
                        )

                    confidence = skill.get(
                        "confidence"
                    )

                    if (
                        confidence is None
                        or not isinstance(
                            confidence,
                            (
                                int,
                                float,
                            ),
                        )
                        or confidence < 0
                        or confidence > 1
                    ):

                        errors.append(
                            f"Skill[{index}] confidence must be between 0 and 1."
                        )

                    sources = skill.get(
                        "sources"
                    )

                    if not isinstance(
                        sources,
                        list,
                    ):

                        errors.append(
                            f"Skill[{index}] sources should be array."
                        )

        # ----------------------------------
        # Optional Warnings
        # ----------------------------------

        if projection.get("headline") is None:

            warnings.append(
                "Headline is not available."
            )

        links = projection.get("links")

        if (
            isinstance(
                links,
                dict,
            )
            and not links.get("portfolio")
        ):

            warnings.append(
                "Portfolio link is not available."
            )

        return ValidationResult(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )