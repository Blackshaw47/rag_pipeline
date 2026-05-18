# src/vector_store.py

from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Tuple

import faiss
import numpy as np


@dataclass
class Document:
    id: int
    text: str
    metadata: dict = field(default_factory=dict)


class FAISSVectorStore:
    """
    Vector store backed by FAISS IndexFlatIP.

    Cosine similarity is achieved by L2-normalizing all vectors before
    insertion and at query time — normalized dot product == cosine similarity.
    This avoids the magnitude sensitivity of Euclidean distance while
    leveraging FAISS's optimized C++ inner product kernels.
    """

    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatIP(dim)
        self._docs: List[Document] = []

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------
    def add(self, embeddings: np.ndarray, documents: List[Document]) -> None:
        normalized = self._normalize(embeddings)
        self.index.add(normalized)
        self._docs.extend(documents)

    # ------------------------------------------------------------------
    # Retrieval
    # ------------------------------------------------------------------
    def search(
        self, query_embedding: np.ndarray, top_k: int = 3
    ) -> List[Tuple[Document, float]]:
        query = self._normalize(query_embedding.reshape(1, -1))
        scores, indices = self.index.search(query, top_k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx != -1:
                results.append((self._docs[idx], float(score)))
        return results

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _normalize(vectors: np.ndarray) -> np.ndarray:
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        return (vectors / (norms + 1e-10)).astype(np.float32)

    def __len__(self) -> int:
        return self.index.ntotal
