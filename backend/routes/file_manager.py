"""
Routes for document management.
Now prevents duplicate file uploads, limits simultaneous uploads,
and ensures filenames are sanitized before saving.
"""

import os
import re
from typing import List

from config.config import TEXT_EXTRACTOR_CONFIG
from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/docs", tags=["Documents"])

UPLOAD_DIR = TEXT_EXTRACTOR_CONFIG.temp_upload_dir
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Limit the number of files that can be uploaded per request
MAX_FILES_PER_UPLOAD = 5


def sanitize_filename(filename: str) -> str:
    """
    Extracts the filename from the given path and sanitizes it.
    - Converts to lowercase.
    - Replaces special characters with underscores.
    - Removes multiple consecutive underscores.
    """
    filename = os.path.basename(filename or "")  # Ensure filename is always a string
    filename = filename.lower()  # Convert to lowercase
    filename = re.sub(r"[^\w\d\-_\.]", "_", filename)  # Replace invalid characters
    filename = re.sub(r"_+", "_", filename)  # Remove multiple underscores
    return filename


@router.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents to the configured upload folder.

    1. Prevent duplicate file names
    2. Limit total files in a single request to MAX_FILES_PER_UPLOAD
    3. Sanitize filenames for safe usage
    """
    if len(files) > MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"You can only upload up to {MAX_FILES_PER_UPLOAD} files at once.",
        )

    saved_files = []
    for file in files:
        sanitized_filename = sanitize_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, sanitized_filename)

        # Check for duplicates
        if os.path.exists(file_path):
            raise HTTPException(
                status_code=400,
                detail=f"File '{sanitized_filename}' already exists. Duplicate upload not allowed.",
            )

        # Save the uploaded file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        saved_files.append(sanitized_filename)

    return {"message": "Files uploaded successfully", "files": saved_files}


@router.get("/list/")
async def list_documents():
    """
    List all documents in the configured upload folder.
    """
    files = os.listdir(UPLOAD_DIR)
    return {"documents": files}


@router.delete("/delete/{filename}")
async def delete_document(filename: str):
    """
    Delete a specific document from the configured upload folder.
    """
    sanitized_filename = sanitize_filename(filename)
    file_path = os.path.join(UPLOAD_DIR, sanitized_filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": f"Deleted {sanitized_filename}"}
