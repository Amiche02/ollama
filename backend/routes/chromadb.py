from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.ragutils.chroma_service import get_chroma_collection, query_by_embedding
from services.ragutils.embedder import EmbeddingService  # Correct import

router = APIRouter(prefix="/chromadb", tags=["ChromaDB"])
embedder = EmbeddingService()  # Ensure correct initialization


class SearchRequest(BaseModel):
    query: str


@router.get("/list/")
async def list_extracted_documents():
    """
    Retrieves a list of all indexed documents from ChromaDB.
    """
    try:
        collection = get_chroma_collection()
        results = collection.get(include=["documents", "metadatas"])

        # Extract document names from metadata
        document_names = set()
        if "metadatas" in results and results["metadatas"]:
            for meta in results["metadatas"]:
                if "filename" in meta:
                    document_names.add(meta["filename"])

        return {"extracted_files": list(document_names)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/query/")
async def search_chromadb(request: SearchRequest):
    """
    Searches in ChromaDB using an embedding of the user-provided query.

    Args:
        request (SearchRequest): JSON payload containing `query`.

    Returns:
        dict: Search results from ChromaDB.
    """
    try:
        # Ensure correct function call for embedding generation
        query_embedding = await embedder.get_embeddings([request.query])  # Fixed method

        if not query_embedding:
            raise HTTPException(
                status_code=500, detail="Failed to generate query embedding."
            )

        results = query_by_embedding(query_embedding[0], n_results=5)  # Query correctly
        return results
    except AttributeError:
        raise HTTPException(
            status_code=500,
            detail="EmbeddingService is missing `get_embeddings`. Ensure it's correctly implemented.",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/{filename}")
async def delete_document_from_chromadb(filename: str):
    """
    Deletes all indexed chunks for a specific document from ChromaDB.

    Args:
        filename (str): The document filename.

    Returns:
        dict: Confirmation message.
    """
    try:
        collection = get_chroma_collection()

        # ✅ FIX: First, retrieve all metadata (WITHOUT `ids` in `include`)
        results = collection.get(include=["metadatas"])

        if "metadatas" not in results or not results["metadatas"]:
            raise HTTPException(
                status_code=404, detail="No documents found in ChromaDB."
            )

        # Extract all IDs associated with the filename
        chunk_ids = []
        for i, meta in enumerate(results["metadatas"]):
            if meta.get("filename") == filename:
                chunk_ids.append(
                    results["ids"][i]
                )  # Fetch correct ID from results["ids"]

        if not chunk_ids:
            raise HTTPException(
                status_code=404, detail=f"No indexed chunks found for '{filename}'."
            )

        # Delete the identified chunks
        collection.delete(ids=chunk_ids)

        return {"message": f"Deleted all indexed chunks for '{filename}'."}

    except KeyError:
        raise HTTPException(
            status_code=500, detail="Unexpected response format from ChromaDB."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear/")
async def clear_chromadb():
    """
    Deletes all stored documents from ChromaDB.
    """
    try:
        collection = get_chroma_collection()

        # Fetch all indexed metadata first (Corrected `include` parameter)
        results = collection.get(include=["metadatas"])

        if "metadatas" not in results or not results["metadatas"]:
            raise HTTPException(
                status_code=404, detail="No documents found in ChromaDB."
            )

        # Extract all document IDs
        all_ids = []
        for meta in results["metadatas"]:
            if "id" in meta:  # Ensure metadata has an "id" key
                all_ids.append(meta["id"])

        if not all_ids:
            raise HTTPException(
                status_code=404, detail="No document IDs found in ChromaDB."
            )

        # Delete all documents
        collection.delete(ids=all_ids)

        return {"message": "ChromaDB cleared successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get/{filename}")
async def get_extracted_text(filename: str):
    """
    Retrieves all text chunks for a given filename from ChromaDB.
    """
    try:
        collection = get_chroma_collection()
        results = collection.get(include=["documents", "metadatas"])

        if "metadatas" not in results or "documents" not in results:
            raise HTTPException(
                status_code=404, detail="No documents found in ChromaDB."
            )

        # Filter documents by filename
        extracted_chunks = [
            results["documents"][i]
            for i, metadata in enumerate(results["metadatas"])
            if metadata.get("filename") == filename
        ]

        if not extracted_chunks:
            raise HTTPException(
                status_code=404, detail=f"File '{filename}' not found in ChromaDB."
            )

        return {"filename": filename, "chunks": extracted_chunks}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
