import json
from src.pipeline import RAGPipeline
from data.corpus import CORPUS

QUERIES = [
    "How does the system handle peak load?",
    "What caching mechanisms are used to improve performance?",
    "How is data consistency maintained across distributed nodes?",
]


def generate_markdown(results: list) -> str:
    lines = [
        "# Retrieval Benchmark: Strategy A vs Strategy B\n\n",
        "> **Strategy A** — Raw Vector Search: embed the query as-is and retrieve nearest neighbors.\n",
        "> **Strategy B** — AI-Enhanced Retrieval: expand the query via a generative model first, then retrieve.\n\n",
        "---\n",
    ]

    for i, r in enumerate(results, 1):
        lines.append(f"\n## Query {i}\n\n")
        lines.append(f"**Input:** `{r['query']}`\n")

        for key in ("strategy_a", "strategy_b"):
            s = r[key]

            lines.append(f"\n### {s['strategy']}\n")

            if s["expanded_query"] != s["original_query"]:
                lines.append(
                    f"> **Expanded query:**  \n> _{s['expanded_query']}_\n\n"
                )

            lines.append("| Rank | Doc ID | Cosine Score | Snippet |\n")
            lines.append("|:----:|:------:|:------------:|---------|\n")

            for c in s["top_chunks"]:
                snip = (
                    c["text_snippet"]
                    .replace("|", "\\|")
                    .replace("\n", " ")
                )

                lines.append(
                    f"| {c['rank']} | "
                    f"{c['doc_id']} | "
                    f"{c['score']:.4f} | "
                    f"{snip} |\n"
                )

        lines.append("\n---\n")

    return "".join(lines)


def main():
    print("Initializing RAG Pipeline...")
    pipeline = RAGPipeline()

    pipeline.ingest(CORPUS)

    print(f"\nRunning benchmark across {len(QUERIES)} queries...\n")

    results = pipeline.benchmark(QUERIES)

    with open("benchmark_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("✓ Saved benchmark_results.json")

    md = generate_markdown(results)

    with open("retrieval_benchmark.md", "w") as f:
        f.write(md)

    print("✓ Saved retrieval_benchmark.md")

    print("\n" + "=" * 70)
    print(md)


if __name__ == "__main__":
    main()
