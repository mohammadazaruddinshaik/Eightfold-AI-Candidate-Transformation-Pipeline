"""
Calculates confidence for a canonical candidate.
"""

from src.models.canonical_candidate import CanonicalCandidate
from src.models.confidence import Confidence
from src.models.identity_match import IdentityMatch


class ConfidenceCalculator:
    """
    Calculates the overall confidence of a merged candidate.
    """

    def calculate(
        self,
        candidate: CanonicalCandidate,
        identity_result: IdentityMatch,
    ) -> CanonicalCandidate:
        """
        Calculate overall confidence based on:

        1. Identity match score (60%)
        2. Profile completeness (40%)
        """

        completeness = self._calculate_profile_completeness(
            candidate,
        )

        overall_score = round(
            (0.6 * identity_result.score)
            + (0.4 * completeness),
            2,
        )

        matched = (
            ", ".join(identity_result.matched_on)
            if identity_result.matched_on
            else "none"
        )

        reason = (
            f"Identity score: {identity_result.score:.2f} "
            f"(matched on {matched}). "
            f"Profile completeness: {completeness:.2f}. "
            f"Overall confidence: {overall_score:.2f}."
        )

        candidate.overall_confidence = Confidence(
            score=overall_score,
            reason=reason,
        )

        return candidate

    def _calculate_profile_completeness(
        self,
        candidate: CanonicalCandidate,
    ) -> float:
        """
        Calculates profile completeness.

        Total Weight = 100
        """

        score = 0

        if candidate.full_name:
            score += 10

        if candidate.emails:
            score += 20

        if candidate.phones:
            score += 20

        if candidate.location:
            score += 5

        if candidate.skills:
            score += 10

        if candidate.experience:
            score += 15

        if candidate.education:
            score += 10

        if (
            candidate.links.linkedin
            or candidate.links.github
            or candidate.links.portfolio
        ):
            score += 10

        return round(score / 100, 2)