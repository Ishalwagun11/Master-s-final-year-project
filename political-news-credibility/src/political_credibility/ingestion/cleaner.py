from bs4 import BeautifulSoup


def clean_rss_summary(value: str | None) -> str:
    if not value:
        return ""
    soup = BeautifulSoup(value, "html.parser")
    return " ".join(soup.get_text(" ").split())

