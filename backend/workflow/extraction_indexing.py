import asyncio
import logging
from typing import Any, Dict, List

from services.ragutils import CustomSegment, EmbeddingService, Indexer, TextExtractor

logger = logging.getLogger(__name__)


class ExtractionIndexingWorkflow:
    """
    Workflow for extracting text from documents, generating embeddings,
    and indexing each document with optional GPU support.
    """

    def __init__(
        self,
        extractor: TextExtractor = None,
        segmenter: CustomSegment = None,
        embedder: EmbeddingService = None,
    ):
        # Allow dependency injection or default to new instances
        self.extractor = extractor if extractor else TextExtractor()
        self.segmenter = segmenter if segmenter else CustomSegment()
        self.embedder = embedder if embedder else EmbeddingService()
        self.indexer = Indexer(segmenter=self.segmenter, embedder=self.embedder)

    async def process_documents(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Process multiple documents concurrently:
          - Extract text from each document
          - Index them (segment + embeddings)

        Args:
            documents (List[Dict[str, Any]]): A list of documents where each dict has:
                {
                  "document_id": str,
                  "file_path": str,
                  "metadata": dict
                }

        Returns:
            List[Dict[str, Any]]: A list of indexed data for all documents.
        """
        # Create a coroutine for each document
        tasks = [self._process_single_document(doc) for doc in documents]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Ensure only valid dictionaries are returned and filter out errors
        final_results: List[Dict[str, Any]] = [
            result for result in results if isinstance(result, dict)
        ]
        return final_results

    async def _process_single_document(
        self, document: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Extract and index a single document.
        This helper method is used by process_documents.

        Args:
            document (Dict[str, Any]): Document data.

        Returns:
            Dict[str, Any]: Indexed data for the document.
        """
        doc_id = document["document_id"]
        file_path = document["file_path"]
        metadata = document.get("metadata", {})

        logger.info(f"Starting extraction and indexing for document: {doc_id}")

        try:
            # 1) Extract text from file
            extraction_result = await self.extractor.extract_text(file_path)
            logger.info(f"Extraction succeeded for document: {doc_id}")

            # 2) Index the document (segments + embeddings)
            indexed_data: Dict[str, Any] = await self.indexer._process_document(
                document_id=doc_id, text=extraction_result.text or "", metadata=metadata
            )

            logger.info(
                f"Document {doc_id} indexed successfully with {len(indexed_data.get('chunks', []))} chunks."
            )
            return indexed_data  # Ensured it's always a Dict[str, Any]

        except Exception as e:
            logger.error(f"Failed to process document {doc_id}: {str(e)}")

            # 🔍 Explicitly return a correctly structured empty dictionary:
            return {"document_id": doc_id, "chunks": [], "error": str(e)}
