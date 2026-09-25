from dataclasses import dataclass


@dataclass(frozen=True)
class HistoricalMatch:
    event_id: str
    similarity: float
    source_accuracy: dict[str, float]


@dataclass(frozen=True)
class SourcePrediction:
    source_id: str
    score: float
    confidence_label: str
    evidence_count: int


def confidence_label(evidence_count: int) -> str:
    if evidence_count <= 3:
        return "low"
    if evidence_count <= 7:
        return "medium"
    return "high"


def rank_sources(matches: list[HistoricalMatch]) -> list[SourcePrediction]:
    totals: dict[str, float] = {}
    counts: dict[str, int] = {}

    for match in matches:
        for source_id, accuracy in match.source_accuracy.items():
            totals[source_id] = totals.get(source_id, 0.0) + accuracy * match.similarity
            counts[source_id] = counts.get(source_id, 0) + 1

    predictions = [
        SourcePrediction(
            source_id=source_id,
            score=totals[source_id] / max(counts[source_id], 1),
            confidence_label=confidence_label(counts[source_id]),
            evidence_count=counts[source_id],
        )
        for source_id in totals
    ]
    return sorted(predictions, key=lambda item: item.score, reverse=True)

