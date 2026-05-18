# src/pipeline.py

from __future__ import annotations
from typing import List

from .embedder import Embedder
from .query_expander import QueryExpander
from .retriever import Retriever
from .vector_store import Document, FAISSVectorStore


class RAGPipeline:
    """
    Orchestrates the full RAG lifecycle:
      1. ingest()  – embed a text corpus and load into the vector store
      2. query()   – run both retrieval strategies on a single query
      3. benchmark() – run query() across multiple queries for comparison
    """

    def __init__(self):
        self.embedder = Embedder()
        self.vector_store = FAISSVectorStore(dim=self.embedder.DIM)
        self.query_expander = QueryExpander()
        self.retriever = Retriever(self.embedder, self.vector_store, self.query_expander)
        self._ingested = False

    # ------------------------------------------------------------------
    # Ingestion
    # ------------------------------------------------------------------
    def ingest(self, corpus: List[str]) -> None:
        """Embed each text chunk and insert into the vector store."""
        documents = [Document(id=i, text=text) for i, text in enumerate(corpus)]
        embeddings = self.embedder.embed(corpus)
        self.vector_store.add(embeddings, documents)
        self._ingested = True
        print(f"[RAGPipeline] Ingested {len(documents)} docs → index size: {len(self.vector_store)}")

    # ------------------------------------------------------------------
    # Query / Benchmark
    # ------------------------------------------------------------------
    def query(self, query: str, top_k: int = 3) -> dict:
        """Run Strategy A and B and return a side-by-side comparison dict."""
        if not self._ingested:
            raise RuntimeError("No documents ingested. Call pipeline.ingest() first.")

        result_a = self.retriever.retrieve_strategy_a(query, top_k=top_k)
        result_b = self.retriever.retrieve_strategy_b(query, top_k=top_k)
        return {
            "query": query,
            "strategy_a": result_a.to_dict(),
            "strategy_b": result_b.to_dict(),
        }

    def benchmark(self, queries: List[str], top_k: int = 3) -> List[dict]:
        """Run query() for every query in the list."""
        return [self.query(q, top_k=top_k) for q in queries]
