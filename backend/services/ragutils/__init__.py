from .chroma_service import (
    get_chroma_collection,
    query_by_embedding,
    upsert_documents_with_embeddings,
)
from .embedder import EmbeddingModel, EmbeddingService
from .indexer import Indexer
from .segment import CustomSegment
from .text_extractor import ExtractionResult, TextExtractor

# UPDATED import to match the class rename
from .web_search import (
    DuckDuckGoSearchService,
    WebSearchService,
)

__all__ = [
    "EmbeddingService",
    "EmbeddingModel",
    "Indexer",
    "CustomSegment",
    "TextExtractor",
    "ExtractionResult",
    "WebSearchService",
    "DuckDuckGoSearchService",
    "get_chroma_collection",
    "upsert_documents_with_embeddings",
    "query_by_embedding",
]
