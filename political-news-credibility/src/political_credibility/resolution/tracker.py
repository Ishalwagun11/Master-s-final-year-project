from dataclasses import dataclass
from datetime import datetime, timedelta, timezone


@dataclass(frozen=True)
class TrackingWindow:
    cluster_id: str
    starts_at: datetime
    ends_at: datetime


def build_tracking_window(cluster_id: str, hours: int = 72) -> TrackingWindow:
    starts_at = datetime.now(timezone.utc)
    return TrackingWindow(
        cluster_id=cluster_id,
        starts_at=starts_at,
        ends_at=starts_at + timedelta(hours=hours),
    )

