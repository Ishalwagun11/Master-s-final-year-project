#!/usr/bin/env python3

import sys
from pathlib import Path

import pandas as pd

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he  # noqa: E402
from political_credibility.events.disagreement import (  # noqa: E402
    sentiment_variance,
    is_high_disagreement,
)
from political_credibility.nlp.sentiment import VaderScorer  # noqa: E402

REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
DISAGREEMENT_THRESHOLD = 0.15


def main() -> None:
    rows = he.flatten_events(he.EVENTS)
    scorer = VaderScorer()

    # ---- Score every article's tone once ----
    for r in rows:
        r["tone"] = scorer.compound(r["article_headline"])

    df = pd.DataFrame(rows)

    # ---- For each event, measure the spread of the 6 outlets' tones ----
    records = []
    for event_id, group in df.groupby("event_id"):
        tones = group["tone"].tolist()
        variance = sentiment_variance(tones)
        records.append({
            "event_id": event_id,
            "event_name": group["event_name"].iloc[0],
            "event_category": group["event_category"].iloc[0],
            "n_sources": len(group),
            "min_tone": round(min(tones), 3),
            "max_tone": round(max(tones), 3),
            "tone_spread": round(max(tones) - min(tones), 3),
            "variance": round(variance, 4),
            "high_disagreement": is_high_disagreement(tones, DISAGREEMENT_THRESHOLD),
        })

    table = pd.DataFrame(records).sort_values("variance", ascending=False).reset_index(drop=True)

    # ---- Save the full ranked table ----
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    table_path = REPORTS_DIR / "rq1_divergence_table.csv"
    table.to_csv(table_path, index=False)

    # ---- Print a readable summary ----
    n_high = int(table["high_disagreement"].sum())
    n_total = len(table)
    print(f"Measured source disagreement across {n_total} events.\n")
    print(f"Events flagged as HIGH disagreement (variance >= {DISAGREEMENT_THRESHOLD}): "
          f"{n_high} of {n_total}\n")

    print(" TOP 5 most divisive events (sources disagreed most)")
    for _, row in table.head(5).iterrows():
        print(f"  [{row['variance']:.3f}] {row['event_name']}  ({row['event_category']})")

    print("\n BOTTOM 5 (sources agreed most)")
    for _, row in table.tail(5).iloc[::-1].iterrows():
        print(f"  [{row['variance']:.3f}] {row['event_name']}  ({row['event_category']})")

    # ---- Disagreement broken down by event type (a nice RQ1 sub-finding) ----
    by_category = (
        table.groupby("event_category")["variance"]
        .mean()
        .sort_values(ascending=False)
        .round(4)
    )
    print("\n Average disagreement by event type")
    for cat, val in by_category.items():
        print(f"  {val:.4f}  {cat}")

    category_path = REPORTS_DIR / "rq1_divergence_by_category.csv"
    by_category.rename("avg_variance").to_csv(category_path)

    # print(f"\nSaved full ranked table to : {table_path}")
    # print(f"Saved by-category summary to: {category_path}")


if __name__ == "__main__":
    main()
