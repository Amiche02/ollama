import argparse
import asyncio
import logging
import os
import sys

import numpy as np

sys.path.append(os.path.abspath(os.path.join(__file__, "../../")))

from services.ragutils.chroma_service import (
    query_by_embedding,
    upsert_documents_with_embeddings,
)
from services.ragutils.embedder import EmbeddingService
from services.ragutils.segment import CustomSegment
from services.ragutils.web_search import DuckDuckGoSearchService
from workflow.extraction_indexing import ExtractionIndexingWorkflow
from workflow.web_search_indexing import WebSearchIndexingWorkflow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

COLLECTION_NAME = "test_rag_collection"


def parse_args():
    """
    Parse command-line arguments to select indexing type.
    """
    parser = argparse.ArgumentParser(
        description="Test ChromaDB indexing with web search or documents."
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Web search mode
    web_parser = subparsers.add_parser("web", help="Run web search indexing.")
    web_parser.add_argument(
        "--query", type=str, required=True, help="Search query for web indexing."
    )

    # Document indexing mode
    docs_parser = subparsers.add_parser("docs", help="Run document indexing.")
    docs_parser.add_argument(
        "--docs", nargs="+", required=True, help="Paths to document files."
    )

    return parser.parse_args()


async def run_web_search(query: str):
    """
    Run web search indexing and store results in ChromaDB.
    """
    logger.info(f"Starting web search for query: '{query}'")

    search_service = DuckDuckGoSearchService(max_results=3)
    segmenter = CustomSegment()
    embedder = EmbeddingService()

    web_search_workflow = WebSearchIndexingWorkflow(
        search_service=search_service, segmenter=segmenter, embedder=embedder
    )
    indexed_data = await web_search_workflow.search_and_index(query)

    if not indexed_data:
        logger.error("Web search indexing returned no results.")
        return

    texts, embeddings, metadatas, ids = [], [], [], []

    for doc in indexed_data:
        for i, chunk in enumerate(doc.get("chunks", [])):
            if (
                isinstance(chunk.get("embedding"), (list, np.ndarray))
                and len(chunk["embedding"]) > 0
            ):
                texts.append(chunk["content"])
                embeddings.append(chunk["embedding"])
                metadatas.append(chunk["metadata"])
                ids.append(f"web_{doc['document_id']}_chunk_{i}")

    if not embeddings:
        logger.warning("No valid embeddings generated. Skipping ChromaDB insertion.")
        return

    upsert_documents_with_embeddings(
        texts, embeddings, metadatas, ids, collection_name=COLLECTION_NAME
    )
    logger.info("Web search data successfully indexed in ChromaDB.")

    results = query_by_embedding(
        embeddings[0], n_results=2, collection_name=COLLECTION_NAME
    )
    logger.info(f"Web search query results: {results}")


async def run_docs_indexing(doc_paths: list[str]):
    """
    Run document extraction workflow and store results in ChromaDB.
    """
    logger.info(f"Starting document processing for {len(doc_paths)} files")

    # Ensure all files exist before processing
    valid_docs: list[dict[str, str | dict[str, str]]] = []
    for path in doc_paths:
        if not os.path.exists(path):
            logger.error(f"File not found: {path}")
        else:
            valid_docs.append(
                {
                    "document_id": f"doc_{len(valid_docs)}",
                    "file_path": path,
                    "metadata": {"title": os.path.basename(path)},
                }
            )

    if not valid_docs:
        logger.error("No valid documents found. Exiting.")
        return

    extraction_workflow = ExtractionIndexingWorkflow()
    indexed_docs = await extraction_workflow.process_documents(valid_docs)

    if not indexed_docs:
        logger.error("Document extraction returned no results.")
        return

    texts, embeddings, metadatas, ids = [], [], [], []

    for doc in indexed_docs:
        if "chunks" not in doc:
            logger.warning(
                f"Skipping document {doc['document_id']} due to missing chunks."
            )
            continue

        for i, chunk in enumerate(doc["chunks"]):
            if (
                isinstance(chunk.get("embedding"), (list, np.ndarray))
                and len(chunk["embedding"]) > 0
            ):
                texts.append(chunk["content"])
                embeddings.append(chunk["embedding"])
                metadatas.append(chunk["metadata"])
                ids.append(f"doc_{doc['document_id']}_chunk_{i}")

    if not embeddings:
        logger.warning("No valid embeddings generated. Skipping ChromaDB insertion.")
        return

    upsert_documents_with_embeddings(
        texts, embeddings, metadatas, ids, collection_name=COLLECTION_NAME
    )
    logger.info("Document data successfully indexed in ChromaDB.")

    results = query_by_embedding(
        embeddings[0], n_results=2, collection_name=COLLECTION_NAME
    )
    logger.info(f"Document query results: {results}")


def main():
    args = parse_args()

    if args.mode == "web":
        asyncio.run(run_web_search(args.query))
    elif args.mode == "docs":
        asyncio.run(run_docs_indexing(args.docs))


if __name__ == "__main__":
    main()
