from apscheduler.schedulers.background import BackgroundScheduler

from political_credibility.ingestion.rss_client import fetch_feed
from political_credibility.ingestion.source_registry import enabled_sources


def collect_once(source_config_path: str) -> list[object]:
    articles: list[object] = []
    for source in enabled_sources(source_config_path):
        articles.extend(fetch_feed(source))
    return articles


def build_scheduler(source_config_path: str, minutes: int = 30) -> BackgroundScheduler:
    scheduler = BackgroundScheduler(timezone="Europe/London")
    scheduler.add_job(
        collect_once,
        "interval",
        minutes=minutes,
        args=[source_config_path],
        id="rss_ingestion",
        replace_existing=True,
    )
    return scheduler

