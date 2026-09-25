from political_credibility.common.settings import get_settings
from political_credibility.ingestion.scheduler import collect_once


def main() -> None:
    settings = get_settings()
    articles = collect_once(settings.source_config)
    print(f"Collected {len(articles)} RSS articles")


if __name__ == "__main__":
    main()

