"""
Regular expression patterns used across parsers.
"""

EMAIL_PATTERN = (
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

PHONE_PATTERN = (
    r"(?:\+?\d{1,3}[\s-]?)?"
    r"(?:\(?\d{3,5}\)?[\s-]?)?"
    r"\d{5}[\s-]?\d{5}"
)

LINKEDIN_PATTERN = (
    r"(?:https?://)?(?:www\.)?linkedin\.com/[^\s|]+"
)

GITHUB_PATTERN = (
    r"(?:https?://)?(?:www\.)?github\.com/[^\s|]+"
)

PORTFOLIO_PATTERN = (
    r"(?:https?://)?(?:www\.)?(?!linkedin|github)[A-Za-z0-9.-]+\.[A-Za-z]{2,}/?[^\s|]*"
)