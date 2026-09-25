"""Light UK-politics keyword filter, shared by the one-shot and scheduled scrapers.

The RSS feeds are already politics-focused, so this is a gentle safety net to drop the
occasional off-topic item — not a strict gate.
"""

POLITICS_KEYWORDS = [
    "parliament", "westminster", "minister", "mp", "labour", "conservative", "tory",
    "lib dem", "snp", "downing street", "prime minister", "chancellor", "cabinet",
    "election", "by-election", "resign", "vote", "commons", "lords", "starmer",
    "sunak", "reform", "government", "policy", "budget", "brexit",
]


def looks_political(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw in text for kw in POLITICS_KEYWORDS)
