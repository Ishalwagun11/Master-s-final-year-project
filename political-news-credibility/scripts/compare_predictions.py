#!/usr/bin/env python3
"""
RQ3: does nearest-neighbour prediction beat a naive baseline?

Compares three ways of answering "which single source should I trust on this event?",
all evaluated the same leave-one-out way (never peeking at the event being predicted):

  1. Nearest-neighbour  — trust the source that did best on the most SIMILAR past events
  2. Naive baseline     — always trust the source with the best OVERALL track record
                          (ignores the specific event — this is RQ3's benchmark)
  3. Random floor       — reference point: pick a source at random

A method "wins" an event if the single source it named was actually TRUE on that event.
If nearest-neighbour beats the naive baseline, event-specific credibility is real and
worth modelling — the central claim of the dissertation.

Usage:
    python scripts/compare_predictions.py
"""
import sys
from pathlib import Path

import pandas as pd

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
PROCESSED_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"
REPORTS_DIR = Path(__file__).resolve().parents[1] / "reports"
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from political_credibility.prediction.event_data import load_events  # noqa: E402
from political_credibility.prediction.nearest_neighbour import HistoricalMatch, rank_sources  # noqa: E402
from political_credibility.nlp.embeddings import cosine_similarity  # noqa: E402

K_NEIGHBOURS = 10


def nearest_neighbour_pick(target, others):
    scored = sorted(others, key=lambda e: cosine_similarity(target.centroid, e.centroid), reverse=True)
    matches = [
        HistoricalMatch(str(n.event_id), cosine_similarity(target.centroid, n.centroid), n.source_accuracy)
        for n in scored[:K_NEIGHBOURS]
    ]
    ranked = rank_sources(matches)
    return ranked[0].source_id if ranked else None


def naive_baseline_pick(others):
    # source with the best OVERALL average accuracy across all other events
    totals, counts = {}, {}
    for e in others:
        for src, acc in e.source_accuracy.items():
            totals[src] = totals.get(src, 0.0) + acc
            counts[src] = counts.get(src, 0) + 1
    if not totals:
        return None
    return max(totals, key=lambda s: totals[s] / counts[s])


def main() -> None:
    events = load_events(PROCESSED_DIR, ROOT_DISSERTATION_DIR)
    n = len(events)
    print(f"Loaded {n} events. Running leave-one-out comparison...\n")

    nn_hits = 0
    baseline_hits = 0
    random_expected = 0.0  # expected accuracy if a source were picked at random
    rows = []

    for target in events:
        others = [e for e in events if e.event_id != target.event_id]

        nn_pick = nearest_neighbour_pick(target, others)
        base_pick = naive_baseline_pick(others)

        nn_ok = nn_pick in target.correct_sources
        base_ok = base_pick in target.correct_sources
        n_sources = len(target.source_accuracy)
        random_expected += (len(target.correct_sources) / n_sources) if n_sources else 0.0

        nn_hits += int(nn_ok)
        baseline_hits += int(base_ok)

        rows.append({
            "event_id": target.event_id,
            "event_name": target.event_name,
            "event_category": target.event_category,
            "nearest_neighbour_pick": nn_pick,
            "nearest_neighbour_correct": nn_ok,
            "naive_baseline_pick": base_pick,
            "naive_baseline_correct": base_ok,
            "actual_correct_sources": ", ".join(sorted(target.correct_sources)) or "(none)",
        })

    nn_acc = nn_hits / n
    base_acc = baseline_hits / n
    random_acc = random_expected / n

    print(f"  Nearest-neighbour : {nn_acc:.1%}")
    print(f"  Naive baseline    : {base_acc:.1%}   (always trust best overall source)")
    print(f"  Random floor      : {random_acc:.1%}   (reference only)")
  
    margin = nn_acc - base_acc
    if margin > 0:
        print(f"\nNearest-neighbour BEATS the naive baseline by {margin*100:.1f} points.")
        print("=> Event-specific credibility carries real, usable signal (supports the thesis).")
    elif margin < 0:
        print(f"\nNaive baseline beats nearest-neighbour by {-margin*100:.1f} points.")
        print("=> On this dataset, overall reliability was enough; event-specific modelling did not help.")
    else:
        print("\nThe two methods tie on this dataset.")

    # ---- Save ----
    # REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    # per_event_path = REPORTS_DIR / "rq3_comparison_per_event.csv"
    # pd.DataFrame(rows).to_csv(per_event_path, index=False)

    # summary = pd.DataFrame([
    #     {"method": "Nearest-neighbour", "accuracy": round(nn_acc, 4)},
    #     {"method": "Naive baseline (best overall source)", "accuracy": round(base_acc, 4)},
    #     {"method": "Random floor", "accuracy": round(random_acc, 4)},
    # ])
    # summary_path = REPORTS_DIR / "rq3_comparison_summary.csv"
    # summary.to_csv(summary_path, index=False)

    # print(f"\nSaved per-event comparison to: {per_event_path}")
    # print(f"Saved summary to             : {summary_path}")


if __name__ == "__main__":
    main()
