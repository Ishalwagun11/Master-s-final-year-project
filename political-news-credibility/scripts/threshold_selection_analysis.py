

import sys
from pathlib import Path

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he
from political_credibility.events.disagreement import sentiment_variance
from political_credibility.nlp.sentiment import VaderScorer
import pandas as pd
import numpy as np


def main():
    rows = he.flatten_events(he.EVENTS)
    scorer = VaderScorer()

    for r in rows:
        r["tone"] = scorer.compound(r["article_headline"])

    df = pd.DataFrame(rows)
    variances = []
    for event_id, group in df.groupby("event_id"):
        tones = group["tone"].tolist()
        variance = sentiment_variance(tones)
        variances.append({
            "event_id": event_id,
            "event_name": group["event_name"].iloc[0],
            "variance": variance,
        })

    variances.sort(key=lambda x: x["variance"])
    all_vars = [v["variance"] for v in variances]
    arr = np.array(all_vars)

   

    # Statistical rules 
    mean_var = arr.mean()
    std_var = arr.std(ddof=1)
    q75 = np.percentile(arr, 75)
    q90 = np.percentile(arr, 90)

    print("VARIANCE THRESHOLD ANALYSIS")
   
    print(f"Mean + 0.5 SD = {mean_var + 0.5 * std_var:.4f}") #Flags events whose variance is moderately above average.
    print(f"75th percentile = {q75:.4f}") #Flags approximately the highest 25% of events.
    print(f"90th percentile = {q90:.4f}") #Flags approximately the highest 10% of events.
    print()

    # Show what each rule flags
    rules = {
        "mean + 0.5 SD": mean_var + 0.5 * std_var,
        "75th percentile": q75,
        "90th percentile": q90,
    }

    print("THRESHOLD COMPARISON:")
    for rule_name, thresh in rules.items():
        flagged = sum(1 for v in all_vars if v >= thresh)
        print(f"  {rule_name:>15}: {thresh:.4f} → {flagged} events ({flagged/44*100:.1f}%)")

    # Our chosen threshold
    thresh_015 = 0.15
    flagged_015 = [v for v in variances if v["variance"] >= thresh_015]

    print()
    print(f"OUR THRESHOLD: {thresh_015}")
    print(f"FLAGGED: {len(flagged_015)} of {len(variances)} events ({len(flagged_015)/44*100:.1f}%)")

    print()
    print("FLAGGED EVENTS:")
    for v in flagged_015:
        print(f"  [{v['variance']:.3f}] {v['event_name']}")

    print()
    


if __name__ == "__main__":
    main()