"""
Routes for text extraction.
Now optionally includes concurrency limit, file limit, and prevents duplicates
if that is desired in the same extraction call.
"""

import asyncio
import os
import shutil
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile
from services.ragutils.text_extractor import TextExtractor

router = APIRouter(prefix="/text-extraction", tags=["Text Extraction"])

# In-memory storage for extracted texts
extracted_texts = {}

# Set the upload directory
UPLOAD_DIR = "docs/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize text extractor
text_extractor = TextExtractor()

# Example concurrency limit
SEM = asyncio.Semaphore(4)

# Limit the number of files per request
MAX_FILES_PER_UPLOAD = 3


@router.post("/extract/")
async def extract_text_from_documents(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents and extract text from them, storing results in memory.

    1. Prevent duplicates if the same file name already exists.
    2. Limit number of files per request with MAX_FILES_PER_UPLOAD.
    3. Use a concurrency limit with a semaphore for CPU-bound extraction.
    """
    if len(files) > MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot process more than {MAX_FILES_PER_UPLOAD} files at once.",
        )

    extracted_results = []

    async def process_file(file: UploadFile):
        # Check duplicates
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        if os.path.exists(file_path):
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' already exists. Duplicate not allowed.",
            )

        # Save file
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # Extract text (concurrency-limited)
        async with SEM:
            extraction_result = await text_extractor.extract_text(file_path)

        extracted_texts[file.filename] = {
            "text": extraction_result.text or "",
            "metadata": extraction_result.metadata,
            "tables_found": (
                len(extraction_result.tables) if extraction_result.tables else 0
            ),
        }

        return {
            "filename": file.filename,
            "text_length": len(extraction_result.text) if extraction_result.text else 0,
            "metadata": extraction_result.metadata,
            "tables_found": (
                len(extraction_result.tables) if extraction_result.tables else 0
            ),
        }

    tasks = [process_file(f) for f in files]

    try:
        results = await asyncio.gather(*tasks)
        extracted_results.extend(results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Text extracted successfully", "results": extracted_results}


@router.get("/list/")
async def list_extracted_texts():
    """
    List all extracted text files stored in memory.
    """
    return {"extracted_files": list(extracted_texts.keys())}


@router.get("/get/{filename}")
async def get_extracted_text(filename: str):
    """
    Retrieve the extracted text of a specific file from memory.
    """
    if filename not in extracted_texts:
        raise HTTPException(status_code=404, detail="Extracted text not found")

    return {"filename": filename, "data": extracted_texts[filename]}


@router.delete("/delete/{filename}")
async def delete_extracted_text(filename: str):
    """
    Delete an extracted text from memory.
    """
    if filename not in extracted_texts:
        raise HTTPException(status_code=404, detail="Extracted text not found")

    del extracted_texts[filename]
    return {"message": f"Deleted extracted text: {filename}"}
