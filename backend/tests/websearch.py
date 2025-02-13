"""
CLI tool for executing a web search workflow and saving results in JSON or Markdown.

Usage:
    python -m pytest backend/tests/websearch.py -- --query "What is AI?"
    # or run it directly (if you prefer) with:
    python backend/tests/websearch.py --query "What is AI?"
"""

import argparse
import asyncio
import json
import logging
import os

from services.ragutils.web_search import (
    DuckDuckGoSearchService,
)
from workflow.web_search_indexing import WebSearchIndexingWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_indexed_data_as_markdown(indexed_data, output_dir="outputs"):
    """
    Saves the indexed data into two separate Markdown (.md) files:
      1. search_results.md  --> The chunk text
      2. embeddings.md      --> The chunk embeddings

    Args:
        indexed_data (list): A list of dictionaries with document data.
        output_dir (str): The directory where to save .md files.
    """
    os.makedirs(output_dir, exist_ok=True)

    search_results_path = os.path.join(output_dir, "search_results.md")
    with open(search_results_path, "w", encoding="utf-8") as sr_file:
        sr_file.write("# Search Results\n\n")
        for doc in indexed_data:
            sr_file.write(f"## Document: {doc['document_id']}\n\n")
            for chunk in doc.get("chunks", []):
                sr_file.write(f"### Chunk #{chunk['chunk_index']}\n")
                sr_file.write(f"{chunk['content']}\n\n")

    embeddings_path = os.path.join(output_dir, "embeddings.md")
    with open(embeddings_path, "w", encoding="utf-8") as emb_file:
        emb_file.write("# Embeddings\n\n")
        for doc in indexed_data:
            emb_file.write(f"## Document: {doc['document_id']}\n\n")
            for chunk in doc.get("chunks", []):
                emb_file.write(f"### Chunk #{chunk['chunk_index']} Embedding\n")
                emb_file.write(f"{chunk['embedding']}\n\n")

    logger.info("Markdown files saved to '%s' directory.", output_dir)


def save_indexed_data_as_json(indexed_data, output_dir="outputs"):
    """
    Saves indexed data into two separate JSON files:
      1. search_results.json --> chunk text & metadata (no embeddings)
      2. embeddings.json     --> embeddings (without full text)

    Args:
        indexed_data (list): A list of dictionaries with document data.
        output_dir (str): The directory where to save .json files.
    """
    os.makedirs(output_dir, exist_ok=True)

    results_data = []
    embeddings_data = []

    for doc in indexed_data:
        doc_id = doc["document_id"]
        results_chunks = []
        embeddings_chunks = []

        for chunk in doc.get("chunks", []):
            results_chunks.append(
                {
                    "chunk_index": chunk["chunk_index"],
                    "content": chunk["content"],
                    "metadata": chunk.get("metadata", {}),
                }
            )
            embedding = chunk["embedding"]
            # Convert to list if it's a numpy or torch tensor
            if hasattr(embedding, "tolist"):
                embedding = embedding.tolist()
            embeddings_chunks.append(
                {"chunk_index": chunk["chunk_index"], "embedding": embedding}
            )

        results_data.append({"document_id": doc_id, "chunks": results_chunks})
        embeddings_data.append({"document_id": doc_id, "chunks": embeddings_chunks})

    results_path = os.path.join(output_dir, "search_results.json")
    embeddings_path = os.path.join(output_dir, "embeddings.json")

    with open(results_path, "w", encoding="utf-8") as f_res:
        json.dump(results_data, f_res, indent=2, ensure_ascii=False)

    with open(embeddings_path, "w", encoding="utf-8") as f_emb:
        json.dump(embeddings_data, f_emb, indent=2, ensure_ascii=False)

    logger.info("Saved search results JSON to: %s", results_path)
    logger.info("Saved embeddings JSON to: %s", embeddings_path)


def parse_args():
    """
    Parse command-line arguments for web search.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="Run web search indexing with a custom query and format options."
    )
    parser.add_argument(
        "--query",
        type=str,
        default="what is artificial intelligence",
        help="The search query to use for web search indexing.",
    )
    parser.add_argument(
        "--save-format",
        choices=["json", "md"],
        default="json",
        help="Format to save the indexed results: 'json' or 'md'.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs/search",
        help="Directory to save the output files.",
    )
    return parser.parse_args()


async def run_workflow(query: str, save_format: str, output_dir: str):
    """
    Execute the web search workflow and save results.

    Args:
        query (str): The search query.
        save_format (str): File format to save the results ('json' or 'md').
        output_dir (str): Output directory path.
    """
    ddg_service = DuckDuckGoSearchService(max_results=3)
    ddg_workflow = WebSearchIndexingWorkflow(search_service=ddg_service)

    indexed_data = await ddg_workflow.search_and_index(query)
    logger.info("DuckDuckGo-based indexing complete.")

    if save_format == "json":
        save_indexed_data_as_json(indexed_data, output_dir=output_dir)
    else:
        save_indexed_data_as_markdown(indexed_data, output_dir=output_dir)


def main():
    """
    Main entry point for this script when run directly.
    """
    args = parse_args()
    query = args.query
    save_format = args.save_format
    output_dir = args.output_dir

    asyncio.run(run_workflow(query, save_format, output_dir))


if __name__ == "__main__":
    main()
