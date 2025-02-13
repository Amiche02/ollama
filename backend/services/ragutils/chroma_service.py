"""
Manages a ChromaDB collection using your custom SentenceTransformer embeddings.
"""

from typing import Any, Dict, List

import chromadb

# Where Chroma will store data
CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "rag_collection"


def get_chroma_collection(collection_name: str = COLLECTION_NAME):
    """
    Returns a Chroma collection, creating one if necessary.
    We'll pass embeddings in manually (rather than using an embedding_function).

    Args:
        collection_name (str): The name of the ChromaDB collection to retrieve or create.

    Returns:
        chromadb.Collection: The ChromaDB collection object.
    """
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_or_create_collection(collection_name)
    return collection


def upsert_documents_with_embeddings(
    texts: List[str],
    embeddings: List[List[float]],
    metadatas: List[Dict[str, Any]],
    ids: List[str],
    collection_name: str = COLLECTION_NAME,
):
    """
    Upserts (adds) text + precomputed embeddings into a ChromaDB collection.

    If documents with the same IDs already exist in ChromaDB, they will be deleted before
    inserting new entries. This prevents duplicate data and ensures the latest embeddings
    are stored.

    Args:
        texts (List[str]): List of document chunks' textual content.
        embeddings (List[List[float]]): List of embedding vectors corresponding to `texts`.
        metadatas (List[Dict[str, Any]]): Metadata associated with each chunk (e.g., source, title).
        ids (List[str]): Unique identifiers for each chunk.
        collection_name (str): The name of the ChromaDB collection where the data will be stored.

    Returns:
        None
    """
    collection = get_chroma_collection(collection_name)

    # Fetch metadata to get existing IDs, since "ids" is not a valid include field
    existing_data = collection.get(include=["metadatas"])

    # Extract existing IDs from metadata if they exist
    existing_ids = set(
        meta["id"] for meta in existing_data.get("metadatas", []) if "id" in meta
    )

    # Identify IDs that are already present in the collection
    ids_to_delete = [doc_id for doc_id in ids if doc_id in existing_ids]

    if ids_to_delete:
        collection.delete(ids=ids_to_delete)
        print(f"Removed {len(ids_to_delete)} old entries before inserting new ones.")

    # Insert new document chunks along with their embeddings and metadata
    collection.add(
        documents=texts,
        embeddings=embeddings,
        metadatas=[{**meta, "id": doc_id} for meta, doc_id in zip(metadatas, ids)],
        ids=ids,
    )

    print(f"Upserted {len(texts)} documents into Chroma collection '{collection_name}'")


def query_by_embedding(
    query_embedding: List[float],
    n_results: int = 5,
    collection_name: str = COLLECTION_NAME,
):
    """
    Query the ChromaDB collection by passing in your precomputed query embedding.

    Args:
        query_embedding (List[float]): Embedding vector for the search query.
        n_results (int): The number of most relevant results to retrieve.
        collection_name (str): The name of the ChromaDB collection to query.

    Returns:
        dict: A dictionary containing the retrieved documents, embeddings, and metadata.
    """
    collection = get_chroma_collection(collection_name)

    # Perform a similarity search in ChromaDB
    results = collection.query(query_embeddings=[query_embedding], n_results=n_results)

    return results
