from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "event_id",
    "event_title",
    "event_date",
    "event_type",
    "outcome_summary",
    "verified_outcome_url",
    "source_id",
    "article_url",
    "article_title",
    "article_summary",
    "initial_frame_label",
    "source_vindicated",
}


def load_historical_csv(path: str | Path) -> pd.DataFrame:
    data = pd.read_csv(path)
    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        missing_list = ", ".join(sorted(missing))
        raise ValueError(f"Historical CSV is missing required columns: {missing_list}")
    return data

