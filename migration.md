### Cosine vs Euclidean Similarity

**Chosen: Cosine Similarity** (via L2-normalized FAISS `IndexFlatIP`).

Cosine similarity measures the **angle** between embedding vectors, making it invariant to vector magnitude. Sentence embeddings encode semantic meaning in their *direction*, not their scale — two paraphrases of the same concept should be close in angle even if their raw magnitudes differ slightly due to tokenization. Euclidean distance conflates magnitude with direction, introducing noise especially when comparing embeddings of varying text lengths. FAISS inner product on L2-normalized vectors is mathematically equivalent to cosine similarity and runs in optimized C++.

### Migration to Vertex AI Vector Search (Matching Engine)

| Step | Local (this repo) | Production (Vertex AI) |
|------|-------------------|------------------------|
| Embeddings | `MockTextEmbeddingModel` (sentence-transformers, 384-dim) | `TextEmbeddingModel.from_pretrained('textembedding-gecko@003')` (768-dim) |
| Vector Index | FAISS `IndexFlatIP` (in-memory) | `aiplatform.MatchingEngineIndex.create_tree_ah_index(dimensions=768)` |
| Index Endpoint | N/A | `MatchingEngineIndexEndpoint.deploy_index()` → `.find_neighbors()` |
| Query Expansion | `MockGenerativeModel` | `vertexai.generative_models.GenerativeModel('gemini-pro')` |
| Ingestion | `index.add()` in-process | `index.upsert_datapoints()` in batches of 10,000 |
| Scaling | Single process | Managed ANN with configurable `num_neighbors` and `fraction_leaf_nodes_to_search` |
