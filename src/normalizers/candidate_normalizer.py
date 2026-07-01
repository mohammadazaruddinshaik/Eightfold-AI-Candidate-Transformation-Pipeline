"""
Candidate normalizer.

Transforms a RawCandidate into a CanonicalCandidate by applying
field-level normalization.
"""
from datetime import datetime

from src.normalizers.country_normalizer import CountryNormalizer
from src.models.canonical_candidate import CanonicalCandidate
from src.models.raw_candidate import RawCandidate
from src.normalizers.email_normalizer import EmailNormalizer
from src.normalizers.phone_normalizer import PhoneNormalizer
from src.models.skill import Skill

class CandidateNormalizer:
    """
    Normalizes a RawCandidate into a CanonicalCandidate.
    """

    def normalize(self, candidate: RawCandidate) -> CanonicalCandidate:
        """
        Normalize a RawCandidate.
        """

        # -----------------------------------------
        # Normalize Experience
        # -----------------------------------------

        normalized_experience = []

        for exp in candidate.experience:

            exp.start = self._normalize_date(exp.start)
            exp.end = self._normalize_date(exp.end)

            normalized_experience.append(exp)

        # -----------------------------------------
        # Normalize Education
        # -----------------------------------------

        normalized_education = []

        for edu in candidate.education:

            edu.start = self._normalize_date(edu.start)
            edu.end = self._normalize_date(edu.end)

            normalized_education.append(edu)

        # -----------------------------------------
        # Build Canonical Candidate
        # -----------------------------------------

        return CanonicalCandidate(

            source=candidate.source,

            full_name=self._normalize_name(candidate.full_name),

            emails=[
                normalized
                for email in candidate.emails
                if (normalized := EmailNormalizer.normalize(email))
            ],

            phones=[
                normalized
                for phone in candidate.phones
                if (normalized := PhoneNormalizer.normalize(phone))
            ],

            location=(
                candidate.location.model_copy(
                    update={
                        "country": CountryNormalizer.normalize(
                            candidate.location.country
                        )
                    }
                )
                if candidate.location
                else None
            ),

            links=candidate.links,

            headline=self._normalize_text(candidate.headline),

            years_experience=candidate.years_experience,

            skills=[
                Skill(
                    name=self._normalize_text(skill),
                    confidence=1.0,
                    sources=[candidate.source],
                )
                for skill in candidate.skills
                if self._normalize_text(skill)
            ],

            experience=normalized_experience,

            education=normalized_education,
        )

    @staticmethod
    def _normalize_name(name: str | None) -> str | None:
        """
        Normalize a candidate's full name.
        """

        if not name:
            return None

        return " ".join(name.split())

    @staticmethod
    def _normalize_text(text: str | None) -> str | None:
        """
        Normalize generic text fields by removing extra whitespace.
        """

        if not text:
            return None

        return " ".join(text.split())
    
    
    @staticmethod
    def _normalize_date(date: str | None) -> str | None:
        """
        Normalize dates to YYYY-MM format.
        """

        if not date:
            return None

        if date.lower() == "present":
            return "Present"

        try:
            return datetime.strptime(
                date.strip(),
                "%b %Y",
            ).strftime("%Y-%m")

        except ValueError:
            return date