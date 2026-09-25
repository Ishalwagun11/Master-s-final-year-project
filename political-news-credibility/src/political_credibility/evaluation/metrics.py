from dataclasses import dataclass


@dataclass(frozen=True)
class ClassificationMetrics:
    accuracy: float
    precision: float
    recall: float


def accuracy_score(expected: list[bool], predicted: list[bool]) -> float:
    if not expected:
        return 0.0
    correct = sum(left == right for left, right in zip(expected, predicted, strict=False))
    return correct / len(expected)

