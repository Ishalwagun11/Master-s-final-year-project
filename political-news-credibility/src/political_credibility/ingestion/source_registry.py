from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class NewsSource:
    id: str
    name: str
    country: str
    politics_feed_url: str | None
    enabled: bool
    notes: str = ""


def load_sources(config_path: str | Path) -> list[NewsSource]:
    payload = yaml.safe_load(Path(config_path).read_text(encoding="utf-8"))
    return [NewsSource(**item) for item in payload.get("sources", [])]


def enabled_sources(config_path: str | Path) -> list[NewsSource]:
    return [
        source
        for source in load_sources(config_path)
        if source.enabled and source.politics_feed_url
    ]

