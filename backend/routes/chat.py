"""
Routes for a Chatbot interface using Ollama.
Provides SSE streaming with no fixed chunk size.
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

# Import the new async functions
from services.ollama import async_chat_with_model, fetch_models

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# In-memory conversation store
conversation_history = []


@router.get("/available_models/")
async def list_available_models():
    """
    Returns the list of available Ollama models.
    This updates dynamically if new models are downloaded to Ollama.
    """
    try:
        models = await fetch_models()
        return {"available_models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/send_message_sse/")
async def send_message_sse(model_name: str, user_message: str):
    """
    Sends a user message to the chosen model and returns the response via SSE streaming.
    No default model is forced; user must supply model_name from /available_models/.
    """
    # Validate requested model
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found in Ollama. Available: {models}",
        )

    # Update conversation in memory
    conversation_history.append({"role": "user", "content": user_message})

    # Format prompt (simple approach: all in one string)
    prompt = "\n".join(
        [
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in conversation_history
        ]
    )

    async def event_generator():
        """
        Generator that streams data in Server-Sent Events (SSE) format.
        """
        try:
            async for chunk in async_chat_with_model(model_name, prompt):
                # SSE format requires `data:` prefix
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            return

    # Also accumulate the final answer at the end so we can store it in memory
    # We'll do a second pass so that we can store the entire text:
    async def capture_response():
        collected_response = []
        try:
            async for chunk in async_chat_with_model(model_name, prompt):
                collected_response.append(chunk)
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"
            return
        # store final
        full_answer = "".join(collected_response)
        conversation_history.append({"role": "ai", "content": full_answer})

    # Return streaming response
    return StreamingResponse(capture_response(), media_type="text/event-stream")


@router.get("/history/")
def get_chat_history():
    """
    Retrieve the full conversation history stored in memory.
    """
    return {"conversation": conversation_history}


@router.delete("/clear_history/")
def clear_chat_history():
    """
    Clear the entire conversation history.
    """
    conversation_history.clear()
    return {"message": "Chat history cleared"}
