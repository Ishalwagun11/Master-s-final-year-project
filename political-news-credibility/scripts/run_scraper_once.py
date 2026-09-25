#!/usr/bin/env python3
"""
The live half of the system: fetch fresh UK political articles from the RSS feeds,
clean them, run the SAME sentiment + embedding steps used on the historical data,
and save the results.

This is one pass of what the scheduler would run every 30 minutes. It demonstrates
that live articles flow through the exact same pipeline the historical events used —
so everything proven on past data (clustering, divergence, forecasting) applies to
them unchanged.

Per-feed error isolation: if one feed is down, the others still run.

Usage:
    python scripts/run_scraper_once.py
"""
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "sources.yaml"
LIVE_DIR = PROJECT_ROOT / "data" / "live"
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from political_credibility.ingestion.source_registry import enabled_sources  # noqa: E402
from political_credibility.ingestion.rss_client import fetch_feed  # noqa: E402
from political_credibility.nlp.sentiment import VaderScorer  # noqa: E402
from political_credibility.nlp.embeddings import MiniLMEmbedder  # noqa: E402

# Light UK-politics keyword filter — the feeds are already politics-focused, so this
# is a gentle safety net to drop the occasional off-topic item, not a strict gate.
POLITICS_KEYWORDS = [
    "parliament", "westminster", "minister", "mp", "labour", "conservative", "tory",
    "lib dem", "snp", "downing street", "prime minister", "chancellor", "cabinet",
    "election", "by-election", "resign", "vote", "commons", "lords", "starmer",
    "sunak", "reform", "government", "policy", "budget", "brexit",
]


def looks_political(title: str, summary: str) -> bool:
    text = (title + " " + summary).lower()
    return any(kw in text for kw in POLITICS_KEYWORDS)


def main() -> None:
    sources = enabled_sources(CONFIG_PATH)
    print(f"Enabled feeds: {[s.id for s in sources]}\n")

    rows = []
    for source in sources:
        try:
            articles = fetch_feed(source)
            kept = [a for a in articles if looks_political(a.title, a.summary)]
            print(f"  {source.id:12s}: fetched {len(articles):3d}, kept {len(kept):3d} political")
            for a in kept:
                rows.append({
                    "source_id": a.source_id,
                    "title": a.title,
                    "summary": a.summary,
                    "url": a.url,
                    "published_at": a.published_at.isoformat() if a.published_at else "",
                    "fetched_at": a.fetched_at.isoformat(),
                })
        except Exception as exc:  # per-feed isolation: one broken feed never stops the rest
            print(f"  {source.id:12s}: FEED ERROR ({type(exc).__name__}) — skipped")

    if not rows:
        print("\nNo articles fetched (feeds may be unreachable from here). "
              "Pipeline ran correctly; there was simply nothing to process.")
        return

    df = pd.DataFrame(rows)

    # ---- SAME NLP as the historical pipeline ----
    print(f"\nRunning sentiment + embeddings on {len(df)} live articles...")
    scorer = VaderScorer()
    df["vader_compound"] = df["title"].apply(scorer.compound)

    embedder = MiniLMEmbedder()
    text_to_embed = (df["title"] + ". " + df["summary"]).tolist()
    vectors = embedder.encode(text_to_embed)

    # ---- Save (metadata as CSV, embeddings as .npy — same format as historical) ----
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_path = LIVE_DIR / f"live_articles_{stamp}.csv"
    npy_path = LIVE_DIR / f"live_embeddings_{stamp}.npy"

    df.to_csv(csv_path, index=False)
    np.save(npy_path, vectors)

    print(f"\nSaved {len(df)} articles to : {csv_path}")
    print(f"Saved embeddings to        : {npy_path}")
    print(f"(row order in the CSV matches row order in the .npy)")

    # ---- Quick peek ----
    print("\nSample of what was collected:")
    for _, r in df.head(5).iterrows():
        print(f"  [{r['source_id']}] {r['title'][:70]}")


if __name__ == "__main__":
    main()
