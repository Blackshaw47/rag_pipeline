# tests/test_pipeline.py

import json
import pytest
from src.pipeline import RAGPipeline
from data.corpus import CORPUS

QUERIES = [
    "How does the system handle peak load?",
    "What caching mechanisms are used to improve performance?",
    "How is data consistency maintained across distributed nodes?",
]


@pytest.fixture(scope="module")
def pipeline():
    p = RAGPipeline()
    p.ingest(CORPUS)
    return p


class TestRAGPipeline:
    def test_ingest_fills_vector_store(self, pipeline):
        assert len(pipeline.vector_store) == len(CORPUS)

    def test_query_before_ingest_raises(self):
        p = RAGPipeline()
        with pytest.raises(RuntimeError, match="No documents ingested"):
            p.query("test")

    def test_query_returns_both_strategies(self, pipeline):
        result = pipeline.query(QUERIES[0])
        assert "strategy_a" in result and "strategy_b" in result

    def test_each_strategy_has_3_chunks(self, pipeline):
        result = pipeline.query(QUERIES[1])
        assert len(result["strategy_a"]["top_chunks"]) == 3
        assert len(result["strategy_b"]["top_chunks"]) == 3

    def test_benchmark_covers_all_queries(self, pipeline):
        results = pipeline.benchmark(QUERIES)
        assert len(results) == len(QUERIES)

    def test_output_is_json_serializable(self, pipeline):
        result = pipeline.query(QUERIES[2])
        json_str = json.dumps(result)   # must not raise
        assert isinstance(json_str, str)

    def test_chunk_scores_are_floats(self, pipeline):
        result = pipeline.query(QUERIES[0])
        for chunk in result["strategy_a"]["top_chunks"]:
            assert isinstance(chunk["score"], float)
