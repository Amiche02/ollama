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
]
