#!/usr/bin/env python3
"""
RQ2: can we forecast which source to trust on a contentious event, by looking at
the most similar PAST events and seeing which source was right on those?

Method (leave-one-out, so we never peek at the event we're predicting):
  for each event:
    1. hide it
    2. find the K most similar OTHER events (cosine similarity of event centroids)
    3. rank sources by similarity-weighted past accuracy (nearest_neighbour.rank_sources)
    4. forecast = the top-ranked source
    5. check: was that source actually TRUE on the hidden event?

Reports overall forecast accuracy + a worked example, and saves both.

Usage:
    python scripts/nearest_neighbour_demo.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from political_credibility.nlp.embeddings import cosine_similarity  # noqa: E402
from political_credibility.prediction.event_data import load_events  # noqa: E402
from political_credibility.prediction.nearest_neighbour import (  # noqa: E402
    HistoricalMatch,
    rank_sources,
)

K_NEIGHBOURS = 10


def forecast_for_event(target, others, k: int):
    """Return the ranked source predictions for one target event."""
    scored = sorted(
        others,
        key=lambda e: cosine_similarity(target.centroid, e.centroid),
        reverse=True,
    )
    neighbours = scored[:k]

    matches = [
        HistoricalMatch(
            event_id=str(n.event_id),
            similarity=cosine_similarity(target.centroid, n.centroid),
            source_accuracy=n.source_accuracy,
        )
        for n in neighbours
    ]
    return rank_sources(matches), neighbours


def main() -> None:
    events = load_events(PROCESSED_DIR, ROOT_DISSERTATION_DIR)
    print(f"Loaded {len(events)} events with embeddings + accuracy labels.\n")

    results = []
    for target in events:
        others = [e for e in events if e.event_id != target.event_id]
        ranked, _ = forecast_for_event(target, others, K_NEIGHBOURS)
        if not ranked:
            continue
        predicted_source = ranked[0].source_id
        was_correct = predicted_source in target.correct_sources
        results.append({
            "event_id": target.event_id,
            "event_name": target.event_name,
            "event_category": target.event_category,
            "predicted_trust_source": predicted_source,
            "predicted_source_was_right": was_correct,
            "actual_correct_sources": ", ".join(sorted(target.correct_sources)) or "(none)",
        })

    table = pd.DataFrame(results)
    accuracy = table["predicted_source_was_right"].mean()

    print("=" * 60)
    print(f"RQ2 forecast accuracy: {accuracy:.1%}")
    print(f"(how often the single source we said to trust was actually correct)")
    print("=" * 60)
    print()

    # ---- Worked example: the most divisive event from RQ1 ----
    example = next((e for e in events if e.event_id == 6), events[0])  # May confidence vote
    ranked, neighbours = forecast_for_event(example, [e for e in events if e.event_id != example.event_id], K_NEIGHBOURS)
    print(f"=== Worked example: {example.event_name} ===")
    print("Most similar past events we based the forecast on:")
    for n in neighbours[:5]:
        sim = cosine_similarity(example.centroid, n.centroid)
        print(f"   {sim:.3f}  {n.event_name}")
    print("\nForecast — who to trust (higher score = more trustworthy on events like this):")
    for pred in ranked[:6]:
        print(f"   {pred.score:.3f}  {pred.source_id}  (confidence: {pred.confidence_label})")
    print(f"\nActually correct on this event: {sorted(example.correct_sources) or '(none)'}")

    # ---- Save ----
    # REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # out_path = REPORTS_DIR / "rq2_nearest_neighbour_results.csv"
    # table.to_csv(out_path, index=False)
    # print(f"\nSaved full per-event results to: {out_path}")


if __name__ == "__main__":
    main()
