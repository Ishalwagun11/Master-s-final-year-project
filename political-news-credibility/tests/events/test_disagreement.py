from political_credibility.events.disagreement import is_high_disagreement, sentiment_variance


def test_sentiment_variance() -> None:
    assert sentiment_variance([0.5, -0.5]) == 0.25


def test_high_disagreement_threshold() -> None:
    assert is_high_disagreement([0.5, -0.5], threshold=0.15)

