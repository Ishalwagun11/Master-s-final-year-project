from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def _load_model(model_name: str = DEFAULT_MODEL_NAME) -> SentenceTransformer:
    # Cached so the ~90MB model is only loaded into memory once per process,
    # not once per article — loading it repeatedly would be far too slow
    # for scoring hundreds of articles.
    return SentenceTransformer(model_name)


class MiniLMEmbedder:
    """Turns article text into 384-number vectors that capture its meaning.

    Two articles about the same real event end up with similar vectors,
    even if they use completely different words — this is what lets us
    group same-event coverage from different outlets without relying on
    manually assigned event IDs.
    """

    def __init__(self, model_name: str = DEFAULT_MODEL_NAME) -> None:
        self._model = _load_model(model_name)

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self._model.get_sentence_embedding_dimension()))
        return self._model.encode(texts, normalize_embeddings=True)

    def encode_one(self, text: str) -> np.ndarray:
        return self.encode([text])[0]


def cosine_similarity(vec_a: np.ndarray, vec_b: np.ndarray) -> float:
    """1.0 = identical meaning, 0.0 = unrelated, -1.0 = opposite meaning."""
    denom = np.linalg.norm(vec_a) * np.linalg.norm(vec_b)
    if denom == 0:
        return 0.0
    return float(np.dot(vec_a, vec_b) / denom)


def similarity_matrix(vectors: np.ndarray) -> np.ndarray:
    """Pairwise cosine similarity between every row in `vectors`.

    Since MiniLMEmbedder.encode() already returns normalized vectors,
    this is just the dot product of the matrix with itself.
    """
    return vectors @ vectors.T

