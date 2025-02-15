import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, List, Optional

import torch
from config.config import AVAILABLE_EMBEDDING_MODELS
from langdetect import DetectorFactory
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

# # Use GPU if available
# DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Force use cpu only
DEVICE = "cpu"


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmbeddingModel(BaseModel):
    """Configuration model for an embedding model."""

    name: str
    language: Optional[List[str]] = None
    model_path: str
    description: Optional[str] = None


class EmbeddingService:
    """Service to manage and generate embeddings using multiple SentenceTransformer models."""

    def __init__(self) -> None:
        """Initializes the EmbeddingService by loading available models and preloading them."""
        self.models: Dict[str, SentenceTransformer] = {}
        self.embedding_models: List[EmbeddingModel] = self._load_available_models()
        self._initialize_models()
        self.executor = ThreadPoolExecutor(max_workers=torch.cuda.device_count() or 4)

    def _load_available_models(self) -> List[EmbeddingModel]:
        """Loads available embedding models from the configuration."""
        embedding_models: List[EmbeddingModel] = []
        for model_dict in AVAILABLE_EMBEDDING_MODELS:
            try:
                model = EmbeddingModel(**model_dict)
                embedding_models.append(model)
                logger.info(f"Loaded embedding model configuration: {model.name}")
            except Exception as e:
                logger.error(
                    f"Error loading embedding model configuration {model_dict}: {str(e)}"
                )
        return embedding_models

    def _initialize_models(self) -> None:
        """Preloads all embedding models to optimize performance during runtime."""
        for model in self.embedding_models:
            try:
                logger.info(f"Loading SentenceTransformer model: {model.name}")
                st_model = SentenceTransformer(
                    model.model_path,
                    device=DEVICE,
                )
                self.models[model.name] = st_model
            except Exception as e:
                logger.error(
                    f"Failed to load SentenceTransformer model {model.name}: {str(e)}"
                )

    def list_models(self) -> List[EmbeddingModel]:
        """Retrieves the list of available embedding models."""
        return self.embedding_models

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generates embeddings for a list of texts using the appropriate models with GPU optimization."""
        if not texts or not all(
            isinstance(text, str) and text.strip() for text in texts
        ):
            return []

        embeddings: List[List[float]] = []

        async def process_batch(
            batch_texts: List[str], model: SentenceTransformer
        ) -> List[List[float]]:
            """Processes a batch of texts asynchronously."""
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(
                self.executor,
                lambda: model.encode(
                    batch_texts, show_progress_bar=False, batch_size=32
                ),
            )

        for text in texts:
            model = self.models[self.embedding_models[0].name]
            batch_embeddings = await process_batch([text], model)
            embeddings.extend(batch_embeddings)

        return embeddings
