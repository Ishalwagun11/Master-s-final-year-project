from pathlib import Path

import pandas as pd


def export_user_study_tasks(events: pd.DataFrame, output_path: str | Path) -> None:
    columns = ["event_id", "event_title", "article_title", "article_summary", "source_id"]
    events.loc[:, columns].to_csv(output_path, index=False)

