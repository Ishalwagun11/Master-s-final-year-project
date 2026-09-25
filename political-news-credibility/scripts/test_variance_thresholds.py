#!/usr/bin/env python3
"""
Test multiple variance thresholds to see how many events get flagged
as "high disagreement" at each level.
"""
import sys
from pathlib import Path

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he
from political_credibility.events.disagreement import sentiment_variance
from political_credibility.nlp.sentiment import VaderScorer

def test_thresholds():
    rows = he.flatten_events(he.EVENTS)
    scorer = VaderScorer()

    # Score every article
    for r in rows:
        r["tone"] = scorer.compound(r["article_headline"])

    # Calculate variance for each event
    event_variances = []
    for event_id, group in pd.DataFrame(rows).groupby("event_id"):
        tones = group["tone"].tolist()
        variance = sentiment_variance(tones)
        event_variances.append({
            "event_id": event_id,
            "event_name": group["event_name"].iloc[0],
            "variance": variance
        })

    # Test multiple thresholds
    thresholds = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    
    print("=" * 60)
    print("TESTING DIFFERENT VARIANCE THRESHOLDS")
    print("=" * 60)
    print(f"\nTotal events: {len(event_variances)}")
    print(f"Variance range: {min(e['variance'] for e in event_variances):.4f} to {max(e['variance'] for e in event_variances):.4f}\n")
    
    print(f"{'Threshold':>10} | {'Events Flagged':>14} | {'Percentage':>10}")
    print("-" * 40)
    
    for thresh in thresholds:
        flagged = sum(1 for e in event_variances if e["variance"] >= thresh)
        pct = flagged / len(event_variances) * 100
        print(f"{thresh:>10.2f} | {flagged:>14} | {pct:>9.1f}%")
    
    print("\n" + "=" * 60)
    print("EVENTS FLAGGED AT 0.15 THRESHOLD:")
    print("=" * 60)
    for e in sorted(event_variances, key=lambda x: x["variance"], reverse=True):
        if e["variance"] >= 0.15:
            print(f"  [{e['variance']:.3f}] {e['event_name']}")
    
    print("\n" + "=" * 60)
    print("EVENTS NOT FLAGGED AT 0.15 THRESHOLD (bottom 5):")
    print("=" * 60)
    for e in sorted(event_variances, key=lambda x: x["variance"])[:5]:
        print(f"  [{e['variance']:.3f}] {e['event_name']}")

if __name__ == "__main__":
    import pandas as pd
    test_thresholds()