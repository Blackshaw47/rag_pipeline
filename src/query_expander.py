# src/query_expander.py

from unittest.mock import MagicMock

# ---------------------------------------------------------------------------
# Deterministic expansion map (simulates a real Gemini Pro response).
# Keys are lowercase substrings of the original query.
# ---------------------------------------------------------------------------
_EXPANSIONS: dict[str, str] = {
    "peak load": (
        "Describe the autoscaling policies, load balancing algorithms, and traffic management "
        "strategies used during high-traffic events and peak load conditions, including horizontal "
        "scaling, request queuing, circuit breaker activation, and Kafka consumer group rebalancing."
    ),
    "caching": (
        "Explain the distributed caching strategies including Redis TTL configuration, write-through "
        "cache invalidation, in-memory cache layers, and how caching reduces PostgreSQL pressure and "
        "improves response latency for frequently accessed API responses and session tokens."
    ),
    "data consistency": (
        "Describe the consistency models (eventual consistency, strong consistency via 2PC), "
        "distributed transaction strategies, vector clock conflict resolution, database read replica "
        "replication lag handling, and last-write-wins approaches across distributed nodes."
    ),
}


class MockGenerativeModel:
    """
    Mocks vertexai.generative_models.GenerativeModel.
    Returns deterministic expansions keyed on query keywords so benchmark
    results are reproducible.
    """

    def __init__(self, model_name: str = "gemini-pro"):
        self.model_name = model_name

    def generate_content(self, prompt: str) -> MagicMock:
        lower = prompt.lower()
        expanded = next(
            (v for k, v in _EXPANSIONS.items() if k in lower),
            # Fallback: append generic technical elaboration
            prompt + " Include architecture details, performance tradeoffs, and failure modes.",
        )
        response = MagicMock()
        response.text = expanded
        return response


class QueryExpander:
    """Wraps MockGenerativeModel and constructs the expansion prompt."""

    SYSTEM_PROMPT = (
        "You are a technical search query optimizer. Rewrite and expand the following query "
        "to improve semantic retrieval from a distributed-systems documentation corpus. "
        "Be specific, include relevant technical terminology, and enumerate key subtopics.\n\n"
        "Original query: {query}\n\nExpanded query:"
    )

    def __init__(self):
        self._model = MockGenerativeModel(model_name="gemini-pro")

    def expand(self, query: str) -> str:
        prompt = self.SYSTEM_PROMPT.format(query=query)
        return self._model.generate_content(prompt).text
