from political_credibility.ingestion.cleaner import clean_rss_summary


def test_clean_rss_summary_removes_html() -> None:
    assert clean_rss_summary("<p>Cabinet <b>minister</b> resigns</p>") == "Cabinet minister resigns"

