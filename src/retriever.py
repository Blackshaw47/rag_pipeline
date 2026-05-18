# src/retriever.py

from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple

from .embedder import Embedder
from .query_expander import QueryExpander
from .vector_store import Document, FAISSVectorStore


@dataclass
class RetrievalResult:
    strategy: str
    original_query: str
    expanded_query: str
    results: List[Tuple[Document, float]]

    def to_dict(self) -> dict:
        return {
            "strategy": self.strategy,
            "original_query": self.original_query,
            "expanded_query": self.expanded_query,
            "top_chunks": [
                {
                    "rank": i + 1,
                    "doc_id": doc.id,
                    "score": round(score, 4),
                    "text_snippet": (
                        doc.text[:160] + "..." if len(doc.text) > 160 else doc.text
                    ),
                }
                for i, (doc, score) in enumerate(self.results)
            ],
        }


class Retriever:
    def __init__(
        self,
        embedder: Embedder,
        vector_store: FAISSVectorStore,
        query_expander: QueryExpander,
    ):
        self.embedder = embedder
        self.vector_store = vector_store
        self.query_expander = query_expander

    def retrieve_strategy_a(self, query: str, top_k: int = 3) -> RetrievalResult:
        """Strategy A: embed the raw query and search directly."""
        emb = self.embedder.embed_single(query)
        results = self.vector_store.search(emb, top_k=top_k)
        return RetrievalResult(
            strategy="A - Raw Vector Search",
            original_query=query,
            expanded_query=query,   # no expansion
            results=results,
        )

    def retrieve_strategy_b(self, query: str, top_k: int = 3) -> RetrievalResult:
        """Strategy B: expand the query first, then embed and search."""
        expanded = self.query_expander.expand(query)
        emb = self.embedder.embed_single(expanded)
        results = self.vector_store.search(emb, top_k=top_k)
        return RetrievalResult(
            strategy="B - AI-Enhanced Retrieval",
            original_query=query,
            expanded_query=expanded,
            results=results,
        )
