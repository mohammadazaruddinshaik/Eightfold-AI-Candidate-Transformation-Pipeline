"""
Identity resolution for canonical candidates.
"""

from src.models.canonical_candidate import CanonicalCandidate
from src.models.identity_match import IdentityMatch


class IdentityResolver:
    """
    Determines whether two canonical candidates represent
    the same individual.
    """

    EMAIL_WEIGHT = 0.40
    PHONE_WEIGHT = 0.40
    GITHUB_WEIGHT = 0.10
    LINKEDIN_WEIGHT = 0.10
    NAME_WEIGHT = 0.20

    MATCH_THRESHOLD = 0.50

    TOTAL_WEIGHT = (
        EMAIL_WEIGHT
        + PHONE_WEIGHT
        + GITHUB_WEIGHT
        + LINKEDIN_WEIGHT
        + NAME_WEIGHT
    )

    def match(
        self,
        first: CanonicalCandidate,
        second: CanonicalCandidate,
    ) -> IdentityMatch:
        """
        Compare two candidates and determine whether they
        represent the same individual.
        """

        matched_weight = 0.0
        matched_on: list[str] = []

        # Email
        if set(first.emails) & set(second.emails):
            matched_weight += self.EMAIL_WEIGHT
            matched_on.append("email")

        # Phone
        if set(first.phones) & set(second.phones):
            matched_weight += self.PHONE_WEIGHT
            matched_on.append("phone")

        # GitHub
        if (
            first.links.github
            and second.links.github
            and first.links.github == second.links.github
        ):
            matched_weight += self.GITHUB_WEIGHT
            matched_on.append("github")

        # LinkedIn
        if (
            first.links.linkedin
            and second.links.linkedin
            and first.links.linkedin == second.links.linkedin
        ):
            matched_weight += self.LINKEDIN_WEIGHT
            matched_on.append("linkedin")

        # Full Name
        if (
            first.full_name
            and second.full_name
            and first.full_name.casefold() == second.full_name.casefold()
        ):
            matched_weight += self.NAME_WEIGHT
            matched_on.append("full_name")

        score = round(
            matched_weight / self.TOTAL_WEIGHT,
            2,
        )

        return IdentityMatch(
            matched=score >= self.MATCH_THRESHOLD,
            score=score,
            matched_on=matched_on,
        )