#!/usr/bin/env python3
"""
Run the live collector automatically every 30 minutes, building up a rolling
48-hour window of articles. The longer it runs, the more multi-source events
appear (because more outlets have covered the same stories over time).

Leave this running in a terminal. It collects once immediately, then every
INTERVAL_MINUTES after that. Press Ctrl+C to stop.

Usage:
    python scripts/run_scheduler.py
    python scripts/run_scheduler.py 15      # custom interval in minutes
"""
import sys
import time
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = PROJECT_ROOT / "configs" / "sources.yaml"
LIVE_DIR = PROJECT_ROOT / "data" / "live"
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from political_credibility.ingestion.collector import collect_live  # noqa: E402

INTERVAL_MINUTES = int(sys.argv[1]) if len(sys.argv) > 1 else 30


def job():
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Collecting...")
    try:
        collect_live(CONFIG_PATH, LIVE_DIR)
    except Exception as exc:
        print(f"Collection failed this cycle ({type(exc).__name__}) — will retry next interval.")


def main() -> None:
    print(f"Live collector scheduled every {INTERVAL_MINUTES} minutes.")
    print("Collecting once now, then on the interval. Press Ctrl+C to stop.\n")

    job()  # run immediately so you don't wait for the first interval

    scheduler = BackgroundScheduler(timezone="Europe/London")
    scheduler.add_job(job, "interval", minutes=INTERVAL_MINUTES, id="live_collect",
                      replace_existing=True)
    scheduler.start()

    try:
        while True:
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        print("\nStopping scheduler...")
        scheduler.shutdown()


if __name__ == "__main__":
    main()
