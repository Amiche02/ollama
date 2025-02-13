"""
Routes for a hybrid RAG + web search approach, with SSE streaming from Ollama.
No default model is forced; user must specify the model name.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from services.ollama import async_chat_with_model, fetch_models
from services.ragutils.chroma_service import get_chroma_collection, query_by_embedding
from services.ragutils.embedder import EmbeddingService
from services.ragutils.web_search import DuckDuckGoSearchService
from workflow.web_search_indexing import WebSearchIndexingWorkflow

router = APIRouter(prefix="/hybrid_chat", tags=["Hybrid Chatbot"])

# In-memory storage for conversation
conversation_history = []
retrieved_context = {}

# Initialize RAG & Web
embedder = EmbeddingService()
search_service = DuckDuckGoSearchService(max_results=3)
web_search_workflow = WebSearchIndexingWorkflow(
    search_service=search_service, segmenter=None, embedder=embedder
)

COLLECTION_NAME = "rag_collection"


@router.get("/available_models/")
async def list_available_models():
    """
    Returns the list of available Ollama models.
    """
    try:
        models = await fetch_models()
        return {"available_models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/clear_chroma/")
async def clear_chroma():
    """
    Completely remove all stored embeddings from ChromaDB.
    """
    try:
        collection = get_chroma_collection(COLLECTION_NAME)
        collection.delete(ids=[])
        return {"message": "All ChromaDB embeddings cleared"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"ChromaDB cleanup failed: {str(e)}"
        )


@router.delete("/delete_document/{doc_id}")
async def delete_document_from_chroma(doc_id: str):
    """
    Remove embeddings related to a specific document from ChromaDB.
    """
    try:
        collection = get_chroma_collection(COLLECTION_NAME)
        doc_results = collection.get(include=["metadatas"])

        ids_to_delete = [
            meta["id"]
            for meta in doc_results.get("metadatas", [])
            if meta.get("id", "").startswith(doc_id)
        ]
        if not ids_to_delete:
            raise HTTPException(
                status_code=404,
                detail=f"No matching document {doc_id} found in ChromaDB",
            )

        collection.delete(ids=ids_to_delete)
        return {"message": f"Deleted document {doc_id} from ChromaDB"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def retrieve_context(query: str) -> list:
    """
    Retrieve the most relevant chunks from ChromaDB. If none found, do a web search.
    """
    global retrieved_context

    # 1) embed user query
    query_embedding = await embedder.get_embeddings([query])

    # 2) query chroma
    rag_results = query_by_embedding(
        query_embedding[0], n_results=3, collection_name=COLLECTION_NAME
    )
    if rag_results["documents"]:
        retrieved_context = {"source": "documents", "data": rag_results["documents"]}
        return rag_results["documents"]

    # 3) fallback to web
    web_results = await web_search_workflow.search_and_index(query)
    retrieved_context = {
        "source": "web_search",
        "data": [r["text"] for r in web_results],
    }
    return retrieved_context["data"]


@router.post("/query_sse/")
async def hybrid_chat_sse(model_name: str, user_message: str):
    """
    SSE streaming version of a hybrid query. No default model used.
    """
    # Validate model
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found in Ollama. Available: {models}",
        )

    # Step 1: get context
    relevant_context = await retrieve_context(user_message)
    context_str = "\n".join(relevant_context)

    # Step 2: record conversation
    conversation_history.append({"role": "user", "content": user_message})

    # Step 3: format prompt
    prompt = f"Context: {context_str}\n\nUser: {user_message}\nAI:"

    async def stream_ollama():
        accumulated_response = []
        try:
            async for chunk in async_chat_with_model(model_name, prompt):
                accumulated_response.append(chunk)
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            return
        # store final answer
        full_answer = "".join(accumulated_response)
        conversation_history.append({"role": "ai", "content": full_answer})

    return StreamingResponse(stream_ollama(), media_type="text/event-stream")


@router.get("/context/")
def get_retrieved_context():
    """
    Retrieve the latest context used to answer.
    """
    return retrieved_context


@router.get("/history/")
def get_chat_history():
    """
    Retrieve the full conversation history for debugging.
    """
    return {"conversation": conversation_history}


@router.delete("/clear_history/")
def clear_chat_history():
    """
    Clear the entire conversation and context.
    """
    conversation_history.clear()
    retrieved_context.clear()
    return {"message": "Chat history and retrieved context cleared"}
