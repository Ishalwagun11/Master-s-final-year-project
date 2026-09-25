import pandas as pd


def overall_source_accuracy(frames: pd.DataFrame) -> pd.DataFrame:
    grouped = frames.groupby("source_id", as_index=False)["source_vindicated"].mean()
    return grouped.rename(columns={"source_vindicated": "overall_accuracy"}).sort_values(
        "overall_accuracy",
        ascending=False,
    )

