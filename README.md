# RAG Pipeline — Semantic Retrieval Engine

**Senior Gen AI Assessment: Semantic RAG & Vector Search**  
Focus: Embeddings · Vector Databases · Retrieval Logic · Benchmarking

---

## Overview

This project implements a **local Retrieval-Augmented Generation (RAG) pipeline** that ingests a technical text corpus, generates embeddings, and benchmarks two retrieval strategies side by side:

| Strategy | Description |
|----------|-------------|
| **A — Raw Vector Search** | Embeds the query as-is and retrieves nearest neighbors via cosine similarity |
| **B — AI-Enhanced Retrieval** | Expands the query through a (mocked) generative model first, then retrieves |

All Vertex AI dependencies (`TextEmbeddingModel`, `GenerativeModel`) are **mocked locally** so the pipeline runs fully offline with no GCP credentials required.

---

## Project Structure

```
rag_pipeline/
├── src/
│   ├── embedder.py          # MockTextEmbeddingModel + Embedder (sentence-transformers backend)
│   ├── vector_store.py      # FAISSVectorStore with cosine similarity (IndexFlatIP + L2-norm)
│   ├── retriever.py         # Retriever: Strategy A and Strategy B logic
│   ├── query_expander.py    # MockGenerativeModel + QueryExpander (deterministic expansions)
│   └── pipeline.py          # RAGPipeline: ingest → query → benchmark orchestration
├── data/
│   └── corpus.py            # 10-document distributed-systems corpus
├── tests/
│   ├── test_embedder.py     # Unit tests for Embedder and MockTextEmbeddingModel
│   ├── test_retriever.py    # Tests for Strategy A & B, including mock SDK verification
│   └── test_pipeline.py     # End-to-end pipeline tests
├── benchmark.py             # Benchmark runner — generates JSON + Markdown reports
├── benchmark_results.json   # Latest benchmark output (JSON)
├── retrieval_benchmark.md   # Latest benchmark output (Markdown table, Strategy A vs B)
├── migration.md             # Similarity metric rationale + Vertex AI migration guide
└── requirements.txt         # Python dependencies
```

---

## Requirements

- Python 3.10+
- pip

No GPU required. No GCP account or credentials needed.

---

## Installation

```bash
# Clone / enter the repo
cd rag_pipeline

# Create and activate a virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

**Dependencies installed:**

| Package | Purpose |
|---------|---------|
| `sentence-transformers==2.7.0` | Local embedding backend (`all-MiniLM-L6-v2`, 384-dim) |
| `faiss-cpu==1.8.0` | In-memory vector index with optimized inner product search |
| `numpy>=1.26.4` | Numerical operations and vector normalization |
| `pytest>=8.2.0` | Test runner |
| `pytest-cov>=5.0.0` | Coverage reporting |

---

## Running the Benchmark

The benchmark ingests the 10-document corpus, runs both strategies on 3 complex queries, and writes results to disk:

```bash
python benchmark.py
```

**Output files generated:**

- `benchmark_results.json` — structured JSON comparison of Strategy A vs B
- `retrieval_benchmark.md` — Markdown table report (also printed to stdout)

**Sample queries benchmarked:**
1. *"How does the system handle peak load?"*
2. *"What caching mechanisms are used to improve performance?"*
3. *"How is data consistency maintained across distributed nodes?"*

---

## Running the Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=src --cov-report=term-missing

# Run a specific test file
pytest tests/test_pipeline.py -v
```

**Test suites:**

| File | Tests Cover |
|------|------------|
| `test_embedder.py` | Embedding shape, unit norm, Vertex AI SDK mock contract |
| `test_retriever.py` | Strategy A/B results, query expansion, mock GenerativeModel call verification |
| `test_pipeline.py` | Full pipeline ingestion, querying, error handling, JSON serializability |

---

## Using the Pipeline Programmatically

```python
from src.pipeline import RAGPipeline
from data.corpus import CORPUS

# Initialize and ingest
pipeline = RAGPipeline()
pipeline.ingest(CORPUS)

# Single query — returns both strategies
result = pipeline.query("How does the system handle peak load?")
print(result["strategy_a"])  # Raw Vector Search results
print(result["strategy_b"])  # AI-Enhanced Retrieval results

# Benchmark multiple queries
results = pipeline.benchmark([
    "How does the system handle peak load?",
    "What caching mechanisms are used to improve performance?",
    "How is data consistency maintained across distributed nodes?",
])
```

---

## Architecture

```
User Query
    │
    ├─── Strategy A ──────────────────────────────────────────────────────┐
    │    Embedder.embed_single(query)                                      │
    │         │                                                            │
    │    FAISSVectorStore.search(embedding, top_k=3)                      │
    │         │                                                            │
    │    → Top-3 docs by cosine similarity                                │
    │                                                                      │
    └─── Strategy B ───────────────────────────────────┐                  │
         QueryExpander.expand(query)                    │                  │
              │  (MockGenerativeModel rewrites query)   │                  │
         Embedder.embed_single(expanded_query)          │                  │
              │                                         │                  │
         FAISSVectorStore.search(embedding, top_k=3)   │                  │
              │                                         │                  │
         → Top-3 docs by cosine similarity ────────────┘                  │
                                                                           │
RAGPipeline.query() ──── returns side-by-side dict ────────────────────────┘
```

**Why Cosine Similarity over Euclidean Distance?**

Sentence embeddings encode meaning in the *direction* of the vector, not the magnitude. Cosine similarity (angle between vectors) is magnitude-invariant, making it robust to differences in text length. Euclidean distance conflates direction with scale, introducing noise. See [`migration.md`](migration.md) for full rationale.

---

## Migrating to Production (Vertex AI Vector Search)

| Component | This Repo (local) | Production (GCP) |
|-----------|-------------------|-----------------|
| Embeddings | `MockTextEmbeddingModel` — `all-MiniLM-L6-v2`, 384-dim | `TextEmbeddingModel.from_pretrained('textembedding-gecko@003')` — 768-dim |
| Vector Index | `faiss.IndexFlatIP` (in-memory) | `aiplatform.MatchingEngineIndex.create_tree_ah_index(dimensions=768)` |
| Query | `index.search()` | `MatchingEngineIndexEndpoint.find_neighbors()` |
| Query Expansion | `MockGenerativeModel` (deterministic) | `vertexai.generative_models.GenerativeModel('gemini-pro')` |
| Ingestion | `index.add()` in-process | `index.upsert_datapoints()` in batches |
| Scaling | Single process | Managed ANN with configurable `num_neighbors` |

See [`migration.md`](migration.md) for the full step-by-step guide.

---

## Assessment Checklist

| Requirement | Status | Location |
|-------------|--------|----------|
| Local embedding model (sentence-transformers) | Done | `src/embedder.py` |
| Mock `TextEmbeddingModel` (Vertex AI SDK shape) | Done | `src/embedder.py` |
| Mock `GenerativeModel` for query expansion | Done | `src/query_expander.py` |
| FAISS vector store with cosine similarity | Done | `src/vector_store.py` |
| RAGPipeline orchestration class | Done | `src/pipeline.py` |
| Strategy A — Raw Vector Search | Done | `src/retriever.py` |
| Strategy B — AI-Enhanced Retrieval | Done | `src/retriever.py` |
| 10-document technical corpus | Done | `data/corpus.py` |
| Benchmark across 3+ queries | Done | `benchmark.py` |
| JSON comparison report | Done | `benchmark_results.json` |
| Markdown comparison report | Done | `retrieval_benchmark.md` |
| Pytest suite with SDK mock verification | Done | `tests/` |
| Similarity metric rationale (Cosine vs Euclidean) | Done | `migration.md` |
| Vertex AI Vector Search migration guide | Done | `migration.md` |
