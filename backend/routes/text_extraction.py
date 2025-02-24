import asyncio
import os
from typing import Dict, List

from config.config import TEXT_EXTRACTOR_CONFIG
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ragutils.chroma_service import upsert_documents_with_embeddings
from services.ragutils.embedder import EmbeddingService
from services.ragutils.segment import CustomSegment
from services.ragutils.text_extractor import TextExtractor

router = APIRouter(prefix="/text-extraction", tags=["Text Extraction"])

UPLOAD_DIR = TEXT_EXTRACTOR_CONFIG.temp_upload_dir
os.makedirs(UPLOAD_DIR, exist_ok=True)

text_extractor = TextExtractor()
embedder = EmbeddingService()
segmenter = CustomSegment()

SEM = asyncio.Semaphore(4)

# ✅ Ensure extracted_texts is defined only once with the correct type annotation
extracted_texts: Dict[str, List[str]] = (
    {}
)  # Dictionary storing extracted text by filename


class ExtractionRequest(BaseModel):
    filenames: List[str]


@router.post("/extract_and_store/")
async def extract_and_store_text(request: ExtractionRequest):
    """
    1️⃣ Extracts text from the provided documents
    2️⃣ Segments text into chunks
    3️⃣ Generates embeddings
    4️⃣ Stores the data in ChromaDB

    Example API request:
    ```json
    {
        "filenames": ["document1.pdf", "notes.md"]
    }
    ```
    """
    filenames = request.filenames

    if not filenames:
        raise HTTPException(status_code=400, detail="No files provided.")

    extracted_results = []

    async def process_file(filename: str):
        file_path = os.path.join(UPLOAD_DIR, filename)

        if not os.path.exists(file_path):
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

        async with SEM:
            extraction_result = await text_extractor.extract_text(file_path)

        # 📝 Segment text into chunks
        chunks = segmenter.hybrid_segmentation(extraction_result.text or "")
        if not chunks:
            return {
                "filename": filename,
                "text_length": 0,
                "status": "No valid content",
            }

        # 🔍 Generate embeddings
        embeddings = await embedder.get_embeddings(chunks)

        # 🗂 Prepare metadata
        metadatas = [
            {"filename": filename, "chunk_index": i} for i in range(len(chunks))
        ]
        chunk_ids = [f"{filename}_chunk_{i}" for i in range(len(chunks))]

        # 📥 Store data in ChromaDB
        upsert_documents_with_embeddings(
            texts=chunks, embeddings=embeddings, metadatas=metadatas, ids=chunk_ids
        )

        return {
            "filename": filename,
            "text_length": len(extraction_result.text) if extraction_result.text else 0,
            "chunks": len(chunks),
            "status": "Indexed in ChromaDB",
        }

    tasks = [process_file(f) for f in filenames]

    try:
        results = await asyncio.gather(*tasks)
        extracted_results.extend(results)
    except HTTPException as http_err:
        raise http_err
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Text extracted, chunked, embedded, and stored in ChromaDB.",
        "results": extracted_results,
    }
