import asyncio
import logging

from services.ragutils.chroma_service import upsert_documents_with_embeddings
from services.ragutils.embedder import EmbeddingService
from services.ragutils.segment import CustomSegment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Indexer:
    """
    Automates indexing by segmenting text, embedding chunks, and organizing data for storage.
    Handles multiple documents asynchronously for high performance.
    """

    def __init__(self, segmenter: CustomSegment, embedder: EmbeddingService):
        """
        Initializes the Indexer with a segmenter and embedder.
        Args:
            segmenter (CustomSegment): An instance of the segmentation service.
            embedder (EmbeddingService): An instance of the embedding service.
        """
        self.segmenter = segmenter
        self.embedder = embedder

    async def _process_document(
        self, document_id: str, text: str, metadata: dict
    ) -> dict:
        """
        Asynchronously processes a single document by:
          1) Segmenting
          2) Embedding
          3) (NEW) Upserting into Chroma
          4) Returning an indexed_data dict
        """
        logger.info(f"Processing document: {document_id}")

        # Step 1: Segment the text into chunks
        chunks = self.segmenter.hybrid_segmentation(text)
        logger.info(f"Document {document_id} segmented into {len(chunks)} chunks.")

        # Check if no chunks => skip upsert entirely
        if not chunks:
            logger.warning(
                f"Document {document_id} has 0 chunks. Skipping embed/upsert."
            )
            # You can return an empty dict or some minimal info:
            return {
                "document_id": document_id,
                "chunks": [],
            }

        # Step 2: Generate embeddings for each chunk asynchronously
        embeddings = await self.embedder.get_embeddings(chunks)
        logger.info(f"Generated embeddings for document {document_id}.")

        # OPTIONAL: Upsert to Chroma
        # Build some metadata list, IDs, etc.
        # e.g. each chunk uses the same base metadata
        chunk_metadatas = []
        chunk_ids = []
        for i, chunk_text in enumerate(chunks):
            chunk_metadatas.append({**metadata, "chunk_index": i})
            chunk_ids.append(f"{document_id}_{i}")

        # Actually upsert
        upsert_documents_with_embeddings(
            texts=chunks,
            embeddings=embeddings,
            metadatas=chunk_metadatas,
            ids=chunk_ids,
        )

        # Step 3: Also build an internal data structure to return
        indexed_data = {
            "document_id": document_id,
            "chunks": [
                {
                    "chunk_index": idx,
                    "content": chunk,
                    "embedding": embedding,  # if you still want to store in your python dict
                    "metadata": chunk_metadatas[idx],
                }
                for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings))
            ],
        }

        logger.info(f"Indexing complete for document: {document_id}")
        return indexed_data

    async def index_documents(self, documents: list) -> list:
        """
        Asynchronously indexes multiple documents.
        Args:
            documents (list): each dict includes:
                - document_id (str)
                - text (str)
                - metadata (dict)

        Returns:
            list: List of indexed data for all documents.
        """
        tasks = [
            self._process_document(doc["document_id"], doc["text"], doc["metadata"])
            for doc in documents
        ]
        return await asyncio.gather(*tasks)
