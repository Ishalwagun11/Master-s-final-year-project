#!/usr/bin/env python3
"""
Close the loop: take the freshly scraped live articles, group them into events,
measure how much the sources disagree, and — for multi-source events — forecast
which source to trust by matching the live event to the historical database.

This runs the WHOLE system end to end on live data:
    live articles -> cluster into events -> divergence (RQ1) -> trust forecast (RQ2)

Uses the most recent snapshot saved by run_scraper_once.py.

Usage:
    python scripts/run_scraper_once.py      # first, to fetch fresh articles
    python scripts/live_pipeline.py         # then this, to process them
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DISSERTATION_ROOT = PROJECT_ROOT.parent
LIVE_DIR = PROJECT_ROOT / "data" / "live"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from political_credibility.events.clusterer import cluster_articles  # noqa: E402
from political_credibility.events.disagreement import sentiment_variance, is_high_disagreement  # noqa: E402
from political_credibility.nlp.embeddings import cosine_similarity  # noqa: E402
from political_credibility.prediction.event_data import load_events  # noqa: E402
from political_credibility.prediction.nearest_neighbour import HistoricalMatch, rank_sources  # noqa: E402

CLUSTER_DISTANCE = 0.40     # same operating point found best in RQ1
MIN_SOURCES = 2             # a cluster needs >= this many outlets to be a comparable "event"
K_NEIGHBOURS = 10


def latest_snapshot():
    csvs = sorted(LIVE_DIR.glob("live_articles_*.csv"))
    if not csvs:
        raise SystemExit("No live snapshot found. Run scripts/run_scraper_once.py first.")
    csv_path = csvs[-1]
    npy_path = LIVE_DIR / csv_path.name.replace("live_articles_", "live_embeddings_").replace(".csv", ".npy")
    return csv_path, npy_path


def forecast_trust(cluster_centroid, historical):
    """Match a live event to the historical DB and rank which source to trust."""
    scored = sorted(historical, key=lambda e: cosine_similarity(cluster_centroid, e.centroid), reverse=True)
    neighbours = scored[:K_NEIGHBOURS]
    matches = [
        HistoricalMatch(str(n.event_id), cosine_similarity(cluster_centroid, n.centroid), n.source_accuracy)
        for n in neighbours
    ]
    return rank_sources(matches), neighbours


def main() -> None:
    csv_path, npy_path = latest_snapshot()
    df = pd.read_csv(csv_path).fillna("")
    vectors = np.load(npy_path)
    print(f"Loaded {len(df)} live articles from {csv_path.name}\n")

    # ---- Step 1: cluster live articles into events ----
    labels = cluster_articles(vectors, distance_threshold=CLUSTER_DISTANCE)
    df["cluster"] = labels
    n_clusters = len(set(labels))
    print(f"Grouped into {n_clusters} candidate events (distance threshold {CLUSTER_DISTANCE}).")

    # ---- Step 2: keep only clusters covered by >= MIN_SOURCES different outlets ----
    multi = []
    for cluster_id, group in df.groupby("cluster"):
        n_sources = group["source_id"].nunique()
        if n_sources >= MIN_SOURCES:
            multi.append((cluster_id, group))

    print(f"{len(multi)} of them are covered by >= {MIN_SOURCES} outlets "
          f"(these are the comparable multi-source events).\n")

    if not multi:
        print("No multi-source events in this snapshot — with only 3 live feeds this is common.")
        print("Try again after more feeds are enabled, or on a bigger news day.")
        return

    # ---- Step 3: for each multi-source live event, divergence + trust forecast ----
    historical = load_events(PROCESSED_DIR, DISSERTATION_ROOT)
    summary_rows = []

    for cluster_id, group in multi:
        idxs = group.index.tolist()
        centroid = vectors[idxs].mean(axis=0)
        tones = group["vader_compound"].tolist()
        variance = sentiment_variance(tones)
        high = is_high_disagreement(tones)

        ranked, neighbours = forecast_trust(centroid, historical)

        print("=" * 70)
        print(f"LIVE EVENT (cluster {cluster_id}) — covered by {group['source_id'].nunique()} outlets")
        print("=" * 70)
        for _, r in group.iterrows():
            print(f"  [{r['source_id']:9s}] (tone {r['vader_compound']:+.2f}) {r['title'][:64]}")
        print(f"\n  Source disagreement (variance): {variance:.3f}  "
              f"-> {'HIGH — sources clash' if high else 'low — broadly agree'}")
        print(f"  Most similar HISTORICAL event : {neighbours[0].event_name} "
              f"({cosine_similarity(centroid, neighbours[0].centroid):.2f})")
        print(f"  Forecast — trust: {ranked[0].source_id}  (confidence {ranked[0].confidence_label})")
        print()

        summary_rows.append({
            "cluster": cluster_id,
            "n_outlets": group["source_id"].nunique(),
            "outlets": ", ".join(sorted(group["source_id"].unique())),
            "sample_headline": group["title"].iloc[0],
            "disagreement_variance": round(variance, 4),
            "high_disagreement": high,
            "closest_historical_event": neighbours[0].event_name,
            "forecast_trust_source": ranked[0].source_id,
        })

    # ---- Save ----
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    out_path = REPORTS_DIR / "live_pipeline_results.csv"
    pd.DataFrame(summary_rows).to_csv(out_path, index=False)
    print(f"Saved live pipeline results to: {out_path}")


if __name__ == "__main__":
    main()
