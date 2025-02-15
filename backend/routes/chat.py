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


@router.post("/message/")
async def send_message(request: ChatRequest):
    """
    Handles AI interaction and integrates results from ChromaDB and web search if enabled.
    """

    model_name = request.model_name
    user_message = request.user_message
    personality = request.personality

    # Check if the model exists
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found. Available models: {models}",
        )

    # 1️⃣ Retrieve system prompt based on personality
    system_prompt = PersonalityConfig.get_prompt(personality)

    # 2️⃣ Perform web search (if enabled)
    web_results = []
    if request.use_web_search:
        search_service = DuckDuckGoSearchService(max_results=3)
        web_search_workflow = WebSearchIndexingWorkflow(search_service=search_service)
        web_results = await web_search_workflow.search_and_index(user_message)

    # 3️⃣ Retrieve ChromaDB results (if enabled)
    chroma_results = []
    if request.use_rag:
        query_embedding = await embedder.get_embeddings([user_message])
        if query_embedding:
            chroma_results = query_by_embedding(query_embedding[0], n_results=5)

    # 4️⃣ Build the context (Web Search + ChromaDB)
    context = ""

    if web_results:
        context += "\n\n🔍 **Web Search Results:**\n" + "\n".join(
            [doc["chunks"][0]["content"] for doc in web_results if doc["chunks"]]
        )

    # Ensure that chroma_results is a dictionary before using `.get()`
    if isinstance(chroma_results, dict):
        chroma_documents = chroma_results.get(
            "documents", [["No relevant document found."]]
        )
    else:
        chroma_documents = [["No relevant document found."]]

    formatted_chroma_docs = [
        str(item)
        for sublist in chroma_documents
        for item in (sublist if isinstance(sublist, list) else [sublist])
    ]
    context += "\n\n📂 **Document Results:**\n" + "\n".join(formatted_chroma_docs)

    # 5️⃣ Add user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # 6️⃣ Create the final prompt
    final_prompt = f"{system_prompt}\n\n### Context:\n{context}\n\n👤 User: {user_message}\n🤖 AI: "

    # 7️⃣ Handle streaming mode
    if request.stream:

        async def event_generator():
            """
            Generator for SSE streaming mode.
            """
            try:
                async for chunk in async_chat_with_model(model_name, final_prompt):
                    yield f"data: {chunk}\n\n"
            except Exception as e:
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    # 8️⃣ Non-streaming mode (full response)
    response_chunks = []
    try:
        async for chunk in async_chat_with_model(model_name, final_prompt):
            response_chunks.append(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model error: {str(e)}")

    # Store AI response in conversation history
    ai_response = "".join(response_chunks)
    conversation_history.append({"role": "ai", "content": ai_response})

    return {"message": ai_response}


@router.get("/history/")
def get_chat_history():
    """
    Retrieves the full conversation history.

    Returns:
        dict: List of all exchanged messages.
    """
    return {"conversation": conversation_history}


@router.delete("/clear_history/")
def clear_chat_history():
    """
    Clears the entire conversation history.

    Returns:
        dict: Confirmation message.
    """
    conversation_history.clear()
    return {"message": "Chat history cleared successfully."}
