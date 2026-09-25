from political_credibility.prediction.nearest_neighbour import HistoricalMatch, rank_sources


def test_rank_sources_orders_by_weighted_accuracy() -> None:
    predictions = rank_sources(
        [
            HistoricalMatch("event_1", 0.9, {"bbc": 1.0, "guardian": 0.0}),
            HistoricalMatch("event_2", 0.8, {"bbc": 1.0, "guardian": 0.5}),
        ]
    )

    assert predictions[0].source_id == "bbc"

