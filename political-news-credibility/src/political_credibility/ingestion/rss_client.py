from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

import feedparser
from tenacity import retry, stop_after_attempt, wait_exponential

from political_credibility.ingestion.cleaner import clean_rss_summary
from political_credibility.ingestion.source_registry import NewsSource


@dataclass(frozen=True)
class RSSArticle:
    source_id: str
    title: str
    summary: str
    url: str
    published_at: datetime | None
    fetched_at: datetime


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=1, max=8))
def fetch_feed(source: NewsSource) -> list[RSSArticle]:
    if not source.politics_feed_url:
        return []

    feed = feedparser.parse(source.politics_feed_url)
    fetched_at = datetime.now(timezone.utc)
    articles: list[RSSArticle] = []

    for entry in feed.entries:
        articles.append(
            RSSArticle(
                source_id=source.id,
                title=getattr(entry, "title", "").strip(),
                summary=clean_rss_summary(getattr(entry, "summary", "")),
                url=getattr(entry, "link", "").strip(),
                published_at=_parse_datetime(getattr(entry, "published", None)),
                fetched_at=fetched_at,
            )
        )

    return articles

