from dataclasses import dataclass

import numpy as np
from sklearn.cluster import AgglomerativeClustering


@dataclass(frozen=True)
class ArticleVector:
    article_id: str
    source_id: str
    embedding: np.ndarray


def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float:
    denominator = np.linalg.norm(left) * np.linalg.norm(right)
    if denominator == 0:
        return 0.0
    return float(np.dot(left, right) / denominator)


def distinct_source_count(articles: list[ArticleVector]) -> int:
    return len({article.source_id for article in articles})


def cluster_articles(vectors: np.ndarray, distance_threshold: float) -> np.ndarray:
    """Group articles into event clusters using their embeddings.

    Two articles end up in the same cluster if their meaning is close enough
    (cosine distance below `distance_threshold`). No need to say in advance
    how many events/clusters exist — the algorithm works that out itself,
    which matters because real breaking news doesn't come with a known
    event count attached.

    Returns an array of cluster labels, one per row in `vectors`
    (e.g. [0, 0, 1, 1, 1, 2, ...] — rows 0 and 1 are one cluster,
    rows 2-4 are another, row 5 is its own cluster, and so on).
    """
    if len(vectors) == 0:
        return np.array([], dtype=int)
    if len(vectors) == 1:
        return np.array([0])

    model = AgglomerativeClustering(
        n_clusters=None,
        metric="cosine",
        linkage="average",
        distance_threshold=distance_threshold,
    )
    return model.fit_predict(vectors)

