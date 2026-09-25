"""Shared helpers that turn the saved embeddings + historical labels into the
inputs the nearest-neighbour forecaster needs.

Two things every event needs for RQ2:
  1. a single vector representing the whole event (so events can be compared) —
     we use the average of that event's 6 source embeddings ("event centroid").
  2. each source's accuracy on that event — TRUE=1.0, PARTIAL=0.5, FALSE=0.0.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

# accuracy score for each label — how "right" a source was on an event
ACCURACY_MAP = {"TRUE": 1.0, "PARTIAL": 0.5, "FALSE": 0.0}


@dataclass(frozen=True)
class Event:
    event_id: int
    event_name: str
    event_category: str
    centroid: np.ndarray               # single vector for the whole event
    source_accuracy: dict[str, float]  # e.g. {"BBC": 0.5, "Times": 1.0, ...}
    correct_sources: set[str]          # sources that were TRUE on this event


def load_events(processed_dir: Path, dissertation_root: Path) -> list[Event]:
    """Build one Event per historical event, joining saved embeddings with labels."""
    vectors = np.load(processed_dir / "article_embeddings.npy")
    metadata = pd.read_csv(processed_dir / "article_embeddings_metadata.csv")

    # source_correct labels live in historical_events.py, keyed by (event_id, source)
    sys.path.insert(0, str(dissertation_root))
    import historical_events as he  # noqa: E402

    label_lookup: dict[tuple[int, str], str] = {}
    category_lookup: dict[int, str] = {}
    name_lookup: dict[int, str] = {}
    for event in he.EVENTS:
        category_lookup[event["event_id"]] = event["event_category"]
        name_lookup[event["event_id"]] = event["event_name"]
        for src in event["sources"]:
            label_lookup[(event["event_id"], src["source_name"])] = src["source_correct"]

    events: list[Event] = []
    for event_id, group in metadata.groupby("event_id"):
        idxs = group["row_index"].tolist()
        centroid = vectors[idxs].mean(axis=0)

        source_accuracy: dict[str, float] = {}
        correct_sources: set[str] = set()
        for _, row in group.iterrows():
            label = label_lookup.get((event_id, row["source_name"]))
            if label is None:
                continue
            source_accuracy[row["source_name"]] = ACCURACY_MAP[label]
            if label == "TRUE":
                correct_sources.add(row["source_name"])

        events.append(Event(
            event_id=int(event_id),
            event_name=name_lookup[event_id],
            event_category=category_lookup[event_id],
            centroid=centroid,
            source_accuracy=source_accuracy,
            correct_sources=correct_sources,
        ))

    return events
