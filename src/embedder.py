# src/embedder.py

import numpy as np
from unittest.mock import MagicMock
from sentence_transformers import SentenceTransformer


class MockTextEmbeddingModel:
    """
    Mocks vertexai.language_models.TextEmbeddingModel.
    Uses sentence-transformers/all-MiniLM-L6-v2 locally to simulate
    textembedding-gecko behavior (normalized 384-dim dense vectors).
    """

    MODEL_NAME = "textembedding-gecko@003"

    def __init__(self, model_name: str = MODEL_NAME):
        self.model_name = model_name
        self._backend = SentenceTransformer("all-MiniLM-L6-v2")

    @classmethod
    def from_pretrained(cls, model_name: str) -> "MockTextEmbeddingModel":
        """Mirrors the Vertex AI SDK classmethod signature."""
        return cls(model_name=model_name)

    def get_embeddings(self, texts: list[str]) -> list:
        """
        Returns a list of mock embedding objects each with a `.values` attribute,
        matching the Vertex AI SDK response contract.
        """
        raw = self._backend.encode(texts, normalize_embeddings=True)
        results = []
        for vec in raw:
            obj = MagicMock()
            obj.values = vec.tolist()
            results.append(obj)
        return results


class Embedder:
    """Public embedding interface used by the pipeline."""

    DIM = 384  # all-MiniLM-L6-v2 output dimension

    def __init__(self, model_name: str = MockTextEmbeddingModel.MODEL_NAME):
        self._model = MockTextEmbeddingModel.from_pretrained(model_name)

    def embed(self, texts: list[str]) -> np.ndarray:
        """Embed a batch of texts → (N, DIM) float32 array."""
        results = self._model.get_embeddings(texts)
        return np.array([r.values for r in results], dtype=np.float32)

    def embed_single(self, text: str) -> np.ndarray:
        """Embed one text → (DIM,) float32 array."""
        return self.embed([text])[0]
