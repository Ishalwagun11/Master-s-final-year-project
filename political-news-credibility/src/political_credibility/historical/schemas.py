from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class HistoricalSourceFrame:
    event_id: str
    source_id: str
    article_url: str
    article_title: str
    article_summary: str
    initial_frame_label: str
    vader_compound: float | None
    source_vindicated: bool | None


@dataclass(frozen=True)
class HistoricalEvent:
    event_id: str
    event_title: str
    event_date: date
    event_type: str
    outcome_summary: str
    verified_outcome_url: str
    frames: list[HistoricalSourceFrame]

