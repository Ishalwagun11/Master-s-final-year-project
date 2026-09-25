#!/usr/bin/env python3
"""
Extended disagreement and accuracy analysis for the dissertation.

Adds three analyses beyond the current RQ1/RQ3 work:

1. Source-pair disagreement by event type
   - For each event type, compute average |tone difference| between every source pair.
   - Reveals which outlet pairs systematically disagree in which categories.

3. Embedding-based semantic divergence
   - For each event, measure average pairwise cosine DISTANCE between the 6 source
     article-summary embeddings (1 - cosine similarity).
   - Compare this with VADER tone variance to see whether tone-only disagreement
     captures the same thing as meaning-based divergence.

6. Accuracy by event type
   - For each event type, report overall accuracy of each source and of the
     nearest-neighbour vs naive-baseline picks.
   - Tests whether event-specific credibility appears in specific categories.

Usage:
    python scripts/extended_disagreement_analysis.py
"""
from __future__ import annotations

import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[1]
PROCESSED_DIR = ROOT_DISSERTATION_DIR / "political-news-credibility" / "data" / "processed"
SRC_DIR = ROOT_DISSERTATION_DIR / "political-news-credibility" / "src"
REPORTS_DIR = ROOT_DISSERTATION_DIR / "political-news-credibility" / "reports"
FIGURES_DIR = ROOT_DISSERTATION_DIR / "political-news-credibility" / "reports" / "figures"

sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(SRC_DIR))

import historical_events as he  # noqa: E402
from political_credibility.nlp.embeddings import MiniLMEmbedder, cosine_similarity  # noqa: E402
from political_credibility.nlp.sentiment import VaderScorer  # noqa: E402
from political_credibility.events.disagreement import sentiment_variance  # noqa: E402
from political_credibility.prediction.event_data import load_events  # noqa: E402
from political_credibility.prediction.nearest_neighbour import HistoricalMatch, rank_sources  # noqa: E402

DISAGREEMENT_THRESHOLD = 0.15
K_NEIGHBOURS = 10
SOURCES = ["BBC", "Guardian", "Reuters", "Sky News", "Telegraph", "Times"]


def tone_pair_disagreement(rows: list[dict]) -> pd.DataFrame:
    """source-pair tone disagreement by event type."""
    scorer = VaderScorer()
    for r in rows:
        r["tone"] = scorer.compound(r["article_headline"])

    df = pd.DataFrame(rows)

    pair_records = []
    for (event_id, event_name, category), group in df.groupby(
        ["event_id", "event_name", "event_category"], sort=False
    ):
        group = group.sort_values("source_name")
        for src_a, src_b in combinations(SOURCES, 2):
            row_a = group[group["source_name"] == src_a]
            row_b = group[group["source_name"] == src_b]
            if row_a.empty or row_b.empty:
                continue
            diff = abs(float(row_a["tone"].iloc[0]) - float(row_b["tone"].iloc[0]))
            pair_records.append({
                "event_id": event_id,
                "event_name": event_name,
                "event_category": category,
                "source_a": src_a,
                "source_b": src_b,
                "abs_tone_diff": diff,
            })

    pair_df = pd.DataFrame(pair_records)

    # Aggregate: average absolute tone difference for each pair, overall and by category
    overall = (
        pair_df.groupby(["source_a", "source_b"])["abs_tone_diff"]
        .mean()
        .reset_index()
        .rename(columns={"abs_tone_diff": "avg_abs_tone_diff"})
        .sort_values("avg_abs_tone_diff", ascending=False)
    )

    by_category = (
        pair_df.groupby(["event_category", "source_a", "source_b"])["abs_tone_diff"]
        .mean()
        .reset_index()
        .rename(columns={"abs_tone_diff": "avg_abs_tone_diff"})
        .sort_values(["event_category", "avg_abs_tone_diff"], ascending=[True, False])
    )

    return pair_df, overall, by_category


def embedding_divergence(rows: list[dict]) -> pd.DataFrame:
    """ embedding-based semantic divergence per event."""
    embedder = MiniLMEmbedder()
    df = pd.DataFrame(rows)

    summaries = df["article_summary"].fillna("").tolist()
    vectors = embedder.encode(summaries)
    df = df.copy().reset_index(drop=True)
    df["embedding"] = list(vectors)

    records = []
    for (event_id, event_name, category), group in df.groupby(
        ["event_id", "event_name", "event_category"], sort=False
    ):
        group = group.sort_values("source_name")
        vecs = np.stack(group["embedding"].tolist())
        # average pairwise cosine distance = 1 - average pairwise cosine similarity
        sims = vecs @ vecs.T
        # upper triangle (excluding diagonal)
        triu_idx = np.triu_indices(sims.shape[0], k=1)
        avg_cosine_distance = float(1 - sims[triu_idx].mean())

        # also compute tone variance for comparison
        scorer = VaderScorer()
        tones = [scorer.compound(h) for h in group["article_headline"].tolist()]
        vader_var = sentiment_variance(tones)

        records.append({
            "event_id": event_id,
            "event_name": event_name,
            "event_category": category,
            "avg_cosine_distance": round(avg_cosine_distance, 4),
            "vader_variance": round(vader_var, 4),
        })

    return pd.DataFrame(records)


def accuracy_by_event_type() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """per-source and per-method accuracy broken down by event type."""
    events = load_events(PROCESSED_DIR, ROOT_DISSERTATION_DIR)

    # Per-source accuracy by category
    source_rows = []
    method_rows = []
    for target in events:
        others = [e for e in events if e.event_id != target.event_id]

        # nearest-neighbour pick
        scored = sorted(
            others,
            key=lambda e: cosine_similarity(target.centroid, e.centroid),
            reverse=True,
        )
        matches = [
            HistoricalMatch(
                str(n.event_id),
                cosine_similarity(target.centroid, n.centroid),
                n.source_accuracy,
            )
            for n in scored[:K_NEIGHBOURS]
        ]
        ranked = rank_sources(matches)
        nn_pick = ranked[0].source_id if ranked else None

        # naive baseline pick
        totals, counts = {}, {}
        for e in others:
            for src, acc in e.source_accuracy.items():
                totals[src] = totals.get(src, 0.0) + acc
                counts[src] = counts.get(src, 0) + 1
        base_pick = max(totals, key=lambda s: totals[s] / counts[s]) if totals else None

        method_rows.append({
            "event_id": target.event_id,
            "event_name": target.event_name,
            "event_category": target.event_category,
            "nearest_neighbour_pick": nn_pick,
            "nearest_neighbour_correct": nn_pick in target.correct_sources,
            "naive_baseline_pick": base_pick,
            "naive_baseline_correct": base_pick in target.correct_sources,
        })

        for src, acc in target.source_accuracy.items():
            source_rows.append({
                "event_id": target.event_id,
                "event_name": target.event_name,
                "event_category": target.event_category,
                "source": src,
                "accuracy": acc,
            })

    source_df = pd.DataFrame(source_rows)
    method_df = pd.DataFrame(method_rows)

    per_source_by_category = (
        source_df.groupby(["event_category", "source"])["accuracy"]
        .mean()
        .reset_index()
        .sort_values(["event_category", "accuracy"], ascending=[True, False])
        .round(4)
    )

    per_source_overall = (
        source_df.groupby("source")["accuracy"]
        .mean()
        .reset_index()
        .rename(columns={"accuracy": "overall_accuracy"})
        .sort_values("overall_accuracy", ascending=False)
        .round(4)
    )

    method_by_category = (
        method_df.groupby("event_category")[
            ["nearest_neighbour_correct", "naive_baseline_correct"]
        ]
        .mean()
        .reset_index()
        .rename(columns={
            "nearest_neighbour_correct": "nearest_neighbour_accuracy",
            "naive_baseline_correct": "naive_baseline_accuracy",
        })
        .round(4)
    )

    return per_source_by_category, per_source_overall, method_by_category


def plot_source_pair_heatmap(pair_overall: pd.DataFrame, output_path: Path) -> None:
    """Save a symmetric heatmap of average absolute tone differences between sources."""
    sources = sorted(set(pair_overall["source_a"]) | set(pair_overall["source_b"]))
    matrix = pd.DataFrame(np.zeros((len(sources), len(sources))), index=sources, columns=sources)

    for _, row in pair_overall.iterrows():
        matrix.loc[row["source_a"], row["source_b"]] = row["avg_abs_tone_diff"]
        matrix.loc[row["source_b"], row["source_a"]] = row["avg_abs_tone_diff"]

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        matrix.astype(float),
        annot=True,
        fmt=".3f",
        cmap="YlOrRd",
        vmin=0,
        vmax=matrix.values.max(),
        square=True,
        linewidths=0.5,
        cbar_kws={"label": "Avg absolute tone difference"},
    )
    plt.title("Source-pair tone disagreement (overall)")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved source-pair heatmap to: {output_path}")


def plot_category_heatmaps(pair_by_category: pd.DataFrame, output_dir: Path) -> None:
    """Save one heatmap per event category."""
    output_dir.mkdir(parents=True, exist_ok=True)
    categories = pair_by_category["event_category"].unique()

    for category in categories:
        cat_df = pair_by_category[pair_by_category["event_category"] == category]
        sources = sorted(set(cat_df["source_a"]) | set(cat_df["source_b"]))
        matrix = pd.DataFrame(np.zeros((len(sources), len(sources))), index=sources, columns=sources)

        for _, row in cat_df.iterrows():
            matrix.loc[row["source_a"], row["source_b"]] = row["avg_abs_tone_diff"]
            matrix.loc[row["source_b"], row["source_a"]] = row["avg_abs_tone_diff"]

        plt.figure(figsize=(8, 6))
        sns.heatmap(
            matrix.astype(float),
            annot=True,
            fmt=".3f",
            cmap="YlOrRd",
            vmin=0,
            vmax=matrix.values.max(),
            square=True,
            linewidths=0.5,
            cbar_kws={"label": "Avg absolute tone difference"},
        )
        plt.title(f"Source-pair tone disagreement — {category}")
        plt.tight_layout()
        safe_cat = category.replace("/", "_")
        plt.savefig(output_dir / f"source_pair_heatmap_{safe_cat}.png", dpi=300)
        plt.close()

    print(f"Saved {len(categories)} category heatmaps to: {output_dir}")


def plot_divergence_scatter(divergence_df: pd.DataFrame, output_path: Path) -> None:
    """Save a scatter plot of semantic distance vs VADER variance, coloured by category."""
    plt.figure(figsize=(10, 7))
    sns.scatterplot(
        data=divergence_df,
        x="avg_cosine_distance",
        y="vader_variance",
        hue="event_category",
        s=100,
        alpha=0.8,
        edgecolor="black",
    )

    corr, pvalue = stats.pearsonr(divergence_df["avg_cosine_distance"], divergence_df["vader_variance"])
    plt.title(f"Semantic distance vs VADER variance per event\n(Pearson r={corr:.3f}, p={pvalue:.4f})")
    plt.xlabel("Average pairwise cosine distance (article-summary embeddings)")
    plt.ylabel("VADER tone variance")
    plt.axhline(DISAGREEMENT_THRESHOLD, color="red", linestyle="--", linewidth=1, alpha=0.6, label=f"VADER threshold ({DISAGREEMENT_THRESHOLD})")
    plt.legend(title="Event category", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved divergence scatter plot to: {output_path}")


def plot_accuracy_heatmap(per_source_by_category: pd.DataFrame, output_path: Path) -> None:
    """Save a heatmap of per-source accuracy by event category."""
    pivot = per_source_by_category.pivot(index="event_category", columns="source", values="accuracy")
    pivot = pivot[[c for c in ["Guardian", "Telegraph", "Sky News", "Times", "Reuters", "BBC"] if c in pivot.columns]]

    plt.figure(figsize=(10, 6))
    sns.heatmap(
        pivot,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=0,
        vmax=1,
        linewidths=0.5,
        cbar_kws={"label": "Accuracy"},
    )
    plt.title("Per-source accuracy by event category")
    plt.xlabel("Source")
    plt.ylabel("Event category")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"Saved accuracy heatmap to: {output_path}")


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    rows = he.flatten_events(he.EVENTS)
    print(f"Loaded {len(rows)} article rows from historical_events.py\n")

    # Analysis 1: source-pair tone disagreement
 
   
    print("Source-pair tone disagreement")
  
    pair_df, pair_overall, pair_by_category = tone_pair_disagreement(rows)
    print("\nTop 10 source pairs by average absolute tone difference (overall):")
    print(pair_overall.head(10).to_string(index=False))

    pair_overall_path = REPORTS_DIR / "extended_source_pair_disagreement_overall.csv"
    pair_by_category_path = REPORTS_DIR / "extended_source_pair_disagreement_by_category.csv"
    pair_overall.to_csv(pair_overall_path, index=False)
    pair_by_category.to_csv(pair_by_category_path, index=False)
    # print(f"\nSaved overall source-pair disagreement to: {pair_overall_path}")
    # print(f"Saved by-category source-pair disagreement to: {pair_by_category_path}")

    print()
    print(" Embedding-based semantic divergence")
    divergence_df = embedding_divergence(rows)

    # Compare with VADER variance
    corr, pvalue = stats.pearsonr(divergence_df["avg_cosine_distance"], divergence_df["vader_variance"])
    print(f"\nPearson correlation (semantic distance vs VADER variance): r={corr:.3f}, p={pvalue:.4f}")

    print("\nTop 10 events by semantic distance:")
    print(
        divergence_df.sort_values("avg_cosine_distance", ascending=False)
        .head(10)[["event_name", "event_category", "avg_cosine_distance", "vader_variance"]]
        .to_string(index=False)
    )

    divergence_path = REPORTS_DIR / "extended_embedding_divergence_per_event.csv"
    divergence_df.to_csv(divergence_path, index=False)
    # print(f"\nSaved per-event embedding divergence to: {divergence_path}")

    print()
    print("Accuracy by event type")
    per_source_by_category, per_source_overall, method_by_category = accuracy_by_event_type()

    print("\nOverall source accuracy:")
    print(per_source_overall.to_string(index=False))

    print("\nNearest-neighbour vs naive baseline accuracy by event category:")
    print(method_by_category.to_string(index=False))

    per_source_by_category_path = REPORTS_DIR / "extended_accuracy_per_source_by_category.csv"
    per_source_overall_path = REPORTS_DIR / "extended_accuracy_per_source_overall.csv"
    method_by_category_path = REPORTS_DIR / "extended_accuracy_method_by_category.csv"
    per_source_by_category.to_csv(per_source_by_category_path, index=False)
    per_source_overall.to_csv(per_source_overall_path, index=False)
    method_by_category.to_csv(method_by_category_path, index=False)
    # print(f"\nSaved per-source by-category accuracy to: {per_source_by_category_path}")
    # print(f"Saved overall per-source accuracy to: {per_source_overall_path}")
    # print(f"Saved method accuracy by category to: {method_by_category_path}")

if __name__ == "__main__":
    main()
