#!/usr/bin/env python3
"""
Demo script for RQ1: turn article summaries into embeddings, then prove
that summaries about the SAME real event end up "closer together" than
summaries about DIFFERENT events.

This is the first real building block for RQ1 (clustering + disagreement
scoring) and RQ2/RQ3 (finding similar past events for nearest-neighbour
prediction).

Usage:
    python scripts/build_embeddings_demo.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

# historical_events.py lives two folders up, in the main Dissertation folder
ROOT_DISSERTATION_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DISSERTATION_DIR))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import historical_events as he  # noqa: E402
from political_credibility.nlp.embeddings import (  # noqa: E402
    MiniLMEmbedder,
    cosine_similarity,
)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "processed"


def main() -> None:
    rows = he.flatten_events(he.EVENTS)
    print(f"Loaded {len(rows)} article rows from historical_events.py")

    embedder = MiniLMEmbedder()
    summaries = [r["article_summary"] for r in rows]

    print("Encoding all article summaries into embeddings (this loads the model once)...")
    vectors = embedder.encode(summaries)
    print(f"Done. Each summary is now a vector of {vectors.shape[1]} numbers.\n")

    # ---- Save every embedding to disk so it can actually be inspected ----
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    vectors_path = OUTPUT_DIR / "article_embeddings.npy"
    metadata_path = OUTPUT_DIR / "article_embeddings_metadata.csv"

    np.save(vectors_path, vectors)

    metadata = pd.DataFrame([
        {
            "row_index": i,
            "event_id": r["event_id"],
            "event_name": r["event_name"],
            "source_name": r["source_name"],
            "article_summary": r["article_summary"],
        }
        for i, r in enumerate(rows)
    ])
    metadata.to_csv(metadata_path, index=False)

    print(f"Saved all {vectors.shape[0]} embeddings to: {vectors_path}")
    print(f"Saved matching metadata to        : {metadata_path}")
    print(f"(row_index in the metadata file lines up with each row of the .npy array)\n")

    # ---- Demo 1: two DIFFERENT outlets covering the SAME event ----
    same_event_rows = [r for r in rows if r["event_id"] == rows[0]["event_id"]]
    a_idx = rows.index(same_event_rows[0])
    b_idx = rows.index(same_event_rows[1])

    same_sim = cosine_similarity(vectors[a_idx], vectors[b_idx])
    print("=== Two DIFFERENT outlets covering the SAME event ===")
    print(f"Event   : {rows[a_idx]['event_name']}")
    print(f"{rows[a_idx]['source_name']:10s}: {rows[a_idx]['article_summary'][:90]}...")
    print(f"{rows[b_idx]['source_name']:10s}: {rows[b_idx]['article_summary'][:90]}...")
    print(f"Cosine similarity: {same_sim:.3f}  (closer to 1.0 = very similar meaning)\n")

    # ---- Demo 2: two summaries about UNRELATED events ----
    different_event_rows = [r for r in rows if r["event_id"] != rows[0]["event_id"]]
    c_idx = rows.index(different_event_rows[0])

    diff_sim = cosine_similarity(vectors[a_idx], vectors[c_idx])
    print("=== Two summaries about DIFFERENT, unrelated events ===")
    print(f"Event A : {rows[a_idx]['event_name']}")
    print(f"Event C : {rows[c_idx]['event_name']}")
    print(f"Cosine similarity: {diff_sim:.3f}  (should be noticeably lower than the same-event pair)\n")

    print("=== Result ===")
    if same_sim > diff_sim:
        print(f"PASS: same-event similarity ({same_sim:.3f}) > different-event similarity ({diff_sim:.3f})")
        print("Embeddings are correctly picking up on shared meaning between articles")
        print("about the same real-world event, even when the wording is different.")
    else:
        print(f"UNEXPECTED: same-event similarity ({same_sim:.3f}) was not higher than "
              f"different-event similarity ({diff_sim:.3f}) for this particular pair.")


if __name__ == "__main__":
    main()
