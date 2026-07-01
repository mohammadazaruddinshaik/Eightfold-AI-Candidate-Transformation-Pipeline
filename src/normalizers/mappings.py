"""
Canonical mappings used during normalization.
"""

COMPANY_ALIASES = {
    "google": "Google",
    "google llc": "Google",
    "google inc": "Google",
    "google inc.": "Google",

    "microsoft": "Microsoft",
    "microsoft corporation": "Microsoft",
    "microsoft corp": "Microsoft",

    "amazon": "Amazon",
    "amazon.com": "Amazon",
    "amazon.com, inc.": "Amazon",

    "meta": "Meta",
    "meta platforms": "Meta",
    "meta platforms inc.": "Meta",
}

SKILL_ALIASES = {
    "reactjs": "React",
    "react.js": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "ts": "TypeScript",
    "golang": "Go",
}