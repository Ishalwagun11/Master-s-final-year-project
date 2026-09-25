from collections import Counter


def majority_label(labels: list[str]) -> str | None:
    if not labels:
        return None
    [(label, count)] = Counter(labels).most_common(1)
    if count < 2:
        return None
    return label

