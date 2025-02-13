"""
Routes for document management.
Now prevents duplicate file uploads and limits the number of simultaneous uploads.
"""

import os
from typing import List

from fastapi import APIRouter, File, HTTPException, UploadFile

router = APIRouter(prefix="/docs", tags=["Documents"])

UPLOAD_DIR = "docs/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Limit the number of files that can be uploaded per request
MAX_FILES_PER_UPLOAD = 5


@router.post("/upload/")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Upload multiple documents to 'uploads/' folder.

    1. Prevent duplicate file names
    2. Limit total files in a single request to MAX_FILES_PER_UPLOAD
    """
    if len(files) > MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"You can only upload up to {MAX_FILES_PER_UPLOAD} files at once.",
        )

    saved_files = []
    for file in files:
        file_path = os.path.join(UPLOAD_DIR, file.filename)

        # Check for duplicates
        if os.path.exists(file_path):
            raise HTTPException(
                status_code=400,
                detail=f"File '{file.filename}' already exists. Duplicate upload not allowed.",
            )

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        saved_files.append(file.filename)

    return {"message": "Files uploaded successfully", "files": saved_files}


@router.get("/list/")
async def list_documents():
    """
    List all documents in the 'uploads/' folder.
    """
    files = os.listdir(UPLOAD_DIR)
    return {"documents": files}


@router.delete("/delete/{filename}")
async def delete_document(filename: str):
    """
    Delete a specific document from the 'uploads/' folder.
    """
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    os.remove(file_path)
    return {"message": f"Deleted {filename}"}
