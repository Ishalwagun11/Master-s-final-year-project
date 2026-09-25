#!/usr/bin/env python3
"""
RQ3 follow-up (a fair, design-aligned check, NOT tuning-to-win):

The whole point of nearest-neighbour is to help on CONTENTIOUS events — where
sources disagree and "who to trust" genuinely varies. On easy events where
everyone agrees, an overall-reliability baseline should be hard to beat.

So instead of judging both methods on all 44 events lumped together, this splits
events by their RQ1 disagreement score and compares the two methods separately on:
  - HIGH-disagreement events (where nearest-neighbour is supposed to earn its keep)
  - LOW-disagreement events (where the baseline is expected to be fine)

Small-sample caution is reported honestly alongside the numbers.

Usage:
    python scripts/compare_by_disagreement.py
"""
import sys
from pathlib import Path

import numpy as np
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
    totals, counts = {}, {}
    for e in others:
        for src, acc in e.source_accuracy.items():
            totals[src] = totals.get(src, 0.0) + acc
            counts[src] = counts.get(src, 0) + 1
    if not totals:
        return None
    return max(totals, key=lambda s: totals[s] / counts[s])


def evaluate_subset(subset, all_events):
    """Leave-one-out over `subset`, but neighbours/baseline drawn from ALL other events."""
    if not subset:
        return None
    nn_hits = base_hits = 0
    for target in subset:
        others = [e for e in all_events if e.event_id != target.event_id]
        nn_hits += int(nearest_neighbour_pick(target, others) in target.correct_sources)
        base_hits += int(naive_baseline_pick(others) in target.correct_sources)
    n = len(subset)
    return {"n": n, "nn_acc": nn_hits / n, "base_acc": base_hits / n}


def main() -> None:
    events = load_events(PROCESSED_DIR, ROOT_DISSERTATION_DIR)

    # attach each event's RQ1 disagreement score (variance of the 6 source accuracies'
    # underlying tone is in the RQ1 table; here we recompute from saved divergence CSV)
    div = pd.read_csv(REPORTS_DIR / "rq1_divergence_table.csv").set_index("event_id")
    for e in events:
        e_variance = float(div.loc[e.event_id, "variance"])
        object.__setattr__(e, "_variance", e_variance)  # frozen dataclass workaround

    ranked_by_var = sorted(events, key=lambda e: e._variance, reverse=True)

    # Split 1: strict threshold (the 5 flagged high-disagreement events)
    high_strict = [e for e in events if e._variance >= 0.15]
    low_strict = [e for e in events if e._variance < 0.15]

    # Split 2: top third vs bottom third (less noisy than 5 events)
    third = len(events) // 3
    high_third = ranked_by_var[:third]
    low_third = ranked_by_var[-third:]

    print("=" * 66)
    print("RQ3 follow-up: does nearest-neighbour help MORE on contentious events?")
    print("=" * 66)

    rows = []
    for label, subset in [
        ("HIGH disagreement (variance >= 0.15)", high_strict),
        ("LOW disagreement (variance < 0.15)", low_strict),
        (f"TOP third by disagreement (n={len(high_third)})", high_third),
        (f"BOTTOM third by disagreement (n={len(low_third)})", low_third),
    ]:
        res = evaluate_subset(subset, events)
        if res is None:
            continue
        margin = res["nn_acc"] - res["base_acc"]
        print(f"\n{label}   [n = {res['n']}]")
        print(f"   Nearest-neighbour : {res['nn_acc']:.1%}")
        print(f"   Naive baseline    : {res['base_acc']:.1%}")
        print(f"   NN minus baseline : {margin*100:+.1f} points")
        rows.append({
            "subset": label,
            "n": res["n"],
            "nearest_neighbour": round(res["nn_acc"], 4),
            "naive_baseline": round(res["base_acc"], 4),
            "nn_minus_baseline": round(margin, 4),
        })

    print("\n" + "=" * 66)
    print("NOTE: the high-disagreement subset is small (n=5), so its numbers move")
    print("in large jumps and should be read as indicative, not conclusive.")
    print("=" * 66)

    out = REPORTS_DIR / "rq3_by_disagreement.csv"
    pd.DataFrame(rows).to_csv(out, index=False)
    print(f"\nSaved to: {out}")


if __name__ == "__main__":
    main()
