# tests/test_embedder.py

import numpy as np
import pytest
from src.embedder import Embedder, MockTextEmbeddingModel


class TestMockTextEmbeddingModel:
    def test_from_pretrained_returns_instance(self):
        m = MockTextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        assert isinstance(m, MockTextEmbeddingModel)

    def test_get_embeddings_count_matches_input(self):
        m = MockTextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        results = m.get_embeddings(["a", "b", "c"])
        assert len(results) == 3

    def test_each_result_has_values_list(self):
        m = MockTextEmbeddingModel.from_pretrained("textembedding-gecko@003")
        results = m.get_embeddings(["hello"])
        assert hasattr(results[0], "values")
        assert isinstance(results[0].values, list)
        assert len(results[0].values) == 384


class TestEmbedder:
    @pytest.fixture
    def embedder(self):
        return Embedder()

    def test_embed_shape(self, embedder):
        embs = embedder.embed(["a", "b", "c"])
        assert embs.shape == (3, 384)

    def test_embed_single_is_1d(self, embedder):
        emb = embedder.embed_single("test")
        assert emb.ndim == 1 and emb.shape[0] == 384

    def test_embeddings_are_unit_norm(self, embedder):
        embs = embedder.embed(["check normalization"])
        norm = np.linalg.norm(embs[0])
        assert abs(norm - 1.0) < 1e-5

    def test_different_texts_differ(self, embedder):
        a = embedder.embed_single("autoscaling kubernetes")
        b = embedder.embed_single("redis cache TTL")
        assert not np.allclose(a, b)
