"""
Enumerations used throughout the candidate transformation pipeline.
"""

from enum import Enum


class SourceType(str, Enum):
    """
    Supported candidate data sources.
    """

    CSV = "csv"
    ATS_JSON = "ats_json"
    RESUME = "resume"
    GITHUB = "github"
    LINKEDIN = "linkedin"
    RECRUITER_NOTES = "recruiter_notes"
    CANONICAL = "canonical"
    
    
class ProvenanceMethod(str, Enum):

    PARSED = "parsed"

    NORMALIZED = "normalized"

    RESOLVED = "resolved"

    MERGED = "merged"

    INFERRED = "inferred"