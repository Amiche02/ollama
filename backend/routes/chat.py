from config.config import PersonalityConfig
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.ollama import async_chat_with_model, fetch_models
from services.ragutils.chroma_service import query_by_embedding
from services.ragutils.embedder import EmbeddingService
from services.ragutils.web_search import DuckDuckGoSearchService
from workflow.web_search_indexing import WebSearchIndexingWorkflow

router = APIRouter(prefix="/chat", tags=["Chatbot"])

embedder = EmbeddingService()

# In-memory conversation storage
conversation_history = []


class ChatRequest(BaseModel):
    model_name: str
    user_message: str
    personality: str = "Universal"
    use_web_search: bool = False
    use_rag: bool = False
    stream: bool = False


@router.get("/available_models/")
async def get_available_models():
    """
    Fetches available models from Ollama.
    """
    try:
        models = await fetch_models()
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/")
async def send_message(request: ChatRequest):
    """
    Main chat endpoint. Handles AI interaction + optional Web Search + optional RAG (ChromaDB).

    Returns:
        {
          "message": <The AI assistant's text>,
          "sources": {
            "web": [...],    # List of web references (title, url)
            "docs": [...]    # List of local doc references (filename, chunk_index, etc.)
          }
        }
    """

    model_name = request.model_name
    user_message = request.user_message
    personality = request.personality

    # 1️⃣ Verify model existence
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found. Available models: {models}",
        )

    # 2️⃣ Grab system prompt based on personality
    system_prompt = PersonalityConfig.get_prompt(personality)

    # These lists will keep track of references for the final API response
    sources_web = []
    sources_docs = []

    # 3️⃣ Optional: perform a web search
    web_results = []
    if request.use_web_search:
        # The web search workflow uses your DuckDuckGoSearchService + indexing
        search_service = DuckDuckGoSearchService(max_results=3)
        web_search_workflow = WebSearchIndexingWorkflow(search_service=search_service)
        # This step does the actual web search + chunking + embedding + storing in Chroma
        web_results = await web_search_workflow.search_and_index(user_message)

        # We can store some references from the web
        for doc in web_results:
            # doc["metadata"] should contain 'title' and 'url'
            meta = doc.get("metadata", {})
            sources_web.append(
                {
                    "title": meta.get("title", "Untitled"),
                    "url": meta.get("url", "No URL"),
                }
            )

    # 4️⃣ Optional: RAG from Chroma
    chroma_results = {}
    if request.use_rag:
        query_embedding = await embedder.get_embeddings([user_message])
        if query_embedding:
            chroma_results = query_by_embedding(query_embedding[0], n_results=5)

    # 5️⃣ Build the text context that the LLM sees
    context = ""

    # 5a) Append web search text
    # Note: web_results come from the indexing workflow, so each doc might have "chunks"
    if web_results:
        context += "\n\n🔍 **Web Search Results:**\n"
        for doc in web_results:
            # Each doc might have a list of chunk objects: doc["chunks"]
            # We'll just grab the first chunk or all of them, depending on your preference
            if "chunks" in doc and doc["chunks"]:
                # e.g. take the first chunk text
                snippet_text = doc["chunks"][0].get("content", "")
                context += f"{snippet_text}\n"

    # 5b) Append ChromaDB doc text
    if isinstance(chroma_results, dict) and chroma_results.get("documents"):
        documents = chroma_results["documents"]  # list of lists of chunk strings
        metadatas = chroma_results["metadatas"]  # parallel list of lists of metadata
        context += "\n\n📂 **Document Results:**\n"

        for i, doc_list in enumerate(documents):
            for j, chunk_text in enumerate(doc_list):
                context += chunk_text + "\n"
                # store references for final JSON
                meta_list = metadatas[i]
                chunk_meta = meta_list[j] if j < len(meta_list) else {}
                sources_docs.append(
                    {
                        "filename": chunk_meta.get("filename", "unknown_file"),
                        "chunk_index": chunk_meta.get("chunk_index", None),
                        "id": chunk_meta.get("id", ""),
                    }
                )

    # 6️⃣ Add user message to conversation history (optional memory)
    conversation_history.append({"role": "user", "content": user_message})

    # 7️⃣ Construct final prompt for the model
    final_prompt = (
        f"{system_prompt}\n\n### Context:\n{context}\n\n"
        f"👤 User: {user_message}\n"
        f"🤖 AI: "
    )

    # 8️⃣ Streaming mode or non-streaming?
    if request.stream:
        # SSE streaming mode
        async def event_generator():
            try:
                async for chunk in async_chat_with_model(model_name, final_prompt):
                    yield f"data: {chunk}\n\n"
            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")
    else:
        # Non-streaming mode: we collect the chunks into one final string
        response_chunks = []
        try:
            async for chunk in async_chat_with_model(model_name, final_prompt):
                response_chunks.append(chunk)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"AI model error: {str(e)}")

        ai_response = "".join(response_chunks)
        # Append the AI's reply to the conversation history
        conversation_history.append({"role": "ai", "content": ai_response})

        # Return both the message + the references as requested
        return {
            "message": ai_response,
            "sources": {"web": sources_web, "docs": sources_docs},
        }


@router.get("/history/")
def get_chat_history():
    """
    Retrieves the full conversation history.
    """
    return {"conversation": conversation_history}


@router.delete("/clear_history/")
def clear_chat_history():
    """
    Clears the entire conversation history.
    """
    conversation_history.clear()
    return {"message": "Chat history cleared successfully."}
