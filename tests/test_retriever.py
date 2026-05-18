# tests/test_retriever.py

import pytest
from unittest.mock import MagicMock
from src.embedder import Embedder
from src.query_expander import QueryExpander
from src.retriever import Retriever
from src.vector_store import Document, FAISSVectorStore
from data.corpus import CORPUS


@pytest.fixture(scope="module")
def retriever():
    embedder = Embedder()
    store = FAISSVectorStore(dim=embedder.DIM)
    expander = QueryExpander()

    docs = [Document(id=i, text=t) for i, t in enumerate(CORPUS)]
    embs = embedder.embed(CORPUS)
    store.add(embs, docs)

    return Retriever(embedder, store, expander)


class TestStrategyA:
    def test_returns_top_k_results(self, retriever):
        r = retriever.retrieve_strategy_a("peak load handling", top_k=3)
        assert len(r.results) == 3

    def test_no_query_expansion(self, retriever):
        q = "database replication"
        r = retriever.retrieve_strategy_a(q, top_k=3)
        assert r.expanded_query == q

    def test_scores_in_valid_range(self, retriever):
        r = retriever.retrieve_strategy_a("caching", top_k=3)
        for _, score in r.results:
            assert -1.0 <= score <= 1.0

    def test_results_sorted_descending(self, retriever):
        r = retriever.retrieve_strategy_a("autoscaling policy", top_k=3)
        scores = [s for _, s in r.results]
        assert scores == sorted(scores, reverse=True)


class TestStrategyB:
    def test_returns_top_k_results(self, retriever):
        r = retriever.retrieve_strategy_b("peak load handling", top_k=3)
        assert len(r.results) == 3

    def test_query_is_expanded(self, retriever):
        q = "How does the system handle peak load?"
        r = retriever.retrieve_strategy_b(q, top_k=3)
        assert r.expanded_query != q
        assert len(r.expanded_query) > len(q)

    def test_mock_generative_model_is_called(self, retriever):
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "expanded: autoscaling circuit breakers load balancing"
        mock_model.generate_content.return_value = mock_response

        original_model = retriever.query_expander._model
        retriever.query_expander._model = mock_model

        retriever.retrieve_strategy_b("peak load", top_k=3)
        mock_model.generate_content.assert_called_once()

        retriever.query_expander._model = original_model  # restore
