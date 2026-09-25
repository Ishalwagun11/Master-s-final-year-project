import sys
from pathlib import Path

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he
import numpy as np
import pandas as pd

from political_credibility.events.disagreement import sentiment_variance
from political_credibility.nlp.sentiment import VaderScorer


# Main threshold used for the current analysis.
PERCENTILE = 90


def main():
    rows = he.flatten_events(he.EVENTS)
    scorer = VaderScorer()

    for row in rows:
        row["tone"] = scorer.compound(row["article_headline"])

    df = pd.DataFrame(rows)
    event_variances = []

    for event_id, group in df.groupby("event_id"):
        tones = group["tone"].tolist()
        event_variances.append({
            "event_id": event_id,
            "event_name": group["event_name"].iloc[0],
            "variance": sentiment_variance(tones),
        })

    variance_values = np.array([event["variance"] for event in event_variances])
    threshold = np.percentile(variance_values, PERCENTILE)
    flagged_events = [
        event for event in event_variances
        if event["variance"] >= threshold
    ]

    flagged_events.sort(key=lambda event: event["variance"], reverse=True)

    print("EMOTIONAL VARIANCE THRESHOLD ANALYSIS")
    print(f"Events analysed: {len(event_variances)}")
    print(f"Selected threshold: {PERCENTILE}th percentile")
    print(f"Variance threshold: {threshold:.4f}")
    print(
        f"Flagged events: {len(flagged_events)} of {len(event_variances)} "
        f"({len(flagged_events) / len(event_variances) * 100:.1f}%)"
    )
    print()
    print("FLAGGED EVENTS:")

    for event in flagged_events:
        print(f"  [{event['variance']:.4f}] {event['event_name']}")


if __name__ == "__main__":
    main()


"""
OPTIONAL ANALYSIS FOR A SEPARATE PAGE

# Compare several percentile thresholds:
for percentile in [75, 80, 85, 90, 95]:
    threshold = np.percentile(variance_values, percentile)
    flagged = sum(value >= threshold for value in variance_values)
    print(percentile, threshold, flagged)

# Mean and standard-deviation thresholds:
mean_variance = variance_values.mean()
standard_deviation = variance_values.std(ddof=1)
for multiplier in [1, 1.5, 2]:
    threshold = mean_variance + multiplier * standard_deviation
    flagged = sum(value >= threshold for value in variance_values)
    print(multiplier, threshold, flagged)

# IQR outlier threshold:
first_quartile = np.percentile(variance_values, 25)
third_quartile = np.percentile(variance_values, 75)
interquartile_range = third_quartile - first_quartile
threshold = third_quartile + 1.5 * interquartile_range
flagged = sum(value >= threshold for value in variance_values)
print(threshold, flagged)

# Largest-gap threshold:
sorted_values = np.sort(variance_values)[::-1]
gaps = sorted_values[:-1] - sorted_values[1:]
largest_gap_index = np.argmax(gaps)
threshold = sorted_values[largest_gap_index + 1]
flagged = sum(value >= threshold for value in variance_values)
print(threshold, flagged)
"""
