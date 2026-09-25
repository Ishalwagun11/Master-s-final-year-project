"""Collect live articles and accumulate them into a rolling 48-hour window.

Why a rolling window: a single scrape returns only what's on the feeds right now, so
few stories are yet covered by multiple outlets. By keeping the last 48 hours of
articles (deduplicated by URL) and re-clustering the whole pool, many more genuine
multi-source events emerge over time. This is also what the dissertation's 48-hour
clustering window calls for.

Each collection:
  1. scrapes the enabled feeds
  2. merges with the existing rolling store, dropping duplicate URLs
  3. prunes anything older than 48 hours
  4. recomputes sentiment + embeddings for the whole window (kept aligned)
  5. saves rolling_articles.csv + rolling_embeddings.npy
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from political_credibility.ingestion.filters import looks_political
from political_credibility.ingestion.rss_client import fetch_feed
from political_credibility.ingestion.source_registry import enabled_sources
from political_credibility.nlp.embeddings import MiniLMEmbedder
from political_credibility.nlp.sentiment import VaderScorer

WINDOW_HOURS = 48


def _scrape(config_path: Path) -> pd.DataFrame:
    rows = []
    for source in enabled_sources(config_path):
        try:
            for a in fetch_feed(source):
                if looks_political(a.title, a.summary):
                    rows.append({
                        "source_id": a.source_id,
                        "title": a.title,
                        "summary": a.summary,
                        "url": a.url,
                        "published_at": a.published_at.isoformat() if a.published_at else "",
                        "fetched_at": a.fetched_at.isoformat(),
                    })
        except Exception as exc:  # per-feed isolation
            print(f"  {source.id}: FEED ERROR ({type(exc).__name__}) — skipped")
    return pd.DataFrame(rows)


def _prune_old(df: pd.DataFrame) -> pd.DataFrame:
    # Retention is based on when WE fetched an article, not its own publish date.
    # This keeps everything collected in the last 48h of operation, so the pool
    # accumulates as the scheduler runs — rather than discarding currently-live
    # articles just because the outlet published them a few days ago.
    cutoff = datetime.now(timezone.utc) - timedelta(hours=WINDOW_HOURS)

    def recently_fetched(row) -> bool:
        try:
            return datetime.fromisoformat(row["fetched_at"]) >= cutoff
        except (ValueError, TypeError):
            return True  # keep if unparseable rather than silently drop

    if df.empty:
        return df
    return df[df.apply(recently_fetched, axis=1)].reset_index(drop=True)


def collect_live(config_path: Path, live_dir: Path) -> dict:
    """Run one collection; returns a small summary dict."""
    live_dir.mkdir(parents=True, exist_ok=True)
    articles_path = live_dir / "rolling_articles.csv"
    embeddings_path = live_dir / "rolling_embeddings.npy"

    fresh = _scrape(config_path)

    if articles_path.exists():
        existing = pd.read_csv(articles_path).fillna("")
        combined = pd.concat([existing[fresh.columns] if not fresh.empty else existing, fresh],
                             ignore_index=True)
    else:
        combined = fresh

    if combined.empty:
        print("No articles collected this run (feeds may be unreachable).")
        return {"total": 0, "new": len(fresh)}

    # dedupe by URL (keep the most recently fetched copy), then prune to the window
    combined = combined.sort_values("fetched_at").drop_duplicates(subset="url", keep="last")
    combined = _prune_old(combined).reset_index(drop=True)

    # recompute sentiment + embeddings for the whole window (stays aligned to the CSV)
    scorer = VaderScorer()
    combined["vader_compound"] = combined["title"].apply(scorer.compound)

    embedder = MiniLMEmbedder()
    vectors = embedder.encode((combined["title"] + ". " + combined["summary"]).tolist())

    combined.to_csv(articles_path, index=False)
    np.save(embeddings_path, vectors)

    print(f"Rolling window now holds {len(combined)} articles "
          f"({len(fresh)} fetched this run) across the last {WINDOW_HOURS}h.")
    return {"total": len(combined), "new": len(fresh)}
