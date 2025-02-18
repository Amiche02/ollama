from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.ollama import async_chat_with_model, fetch_models

router = APIRouter(prefix="/chat", tags=["Chatbot"])

# In-memory conversation storage
conversation_history = []


class ChatRequest(BaseModel):
    model_name: str
    user_message: str


@router.get("/available_models/")
async def list_available_models():
    """
    Retrieves the list of available AI models in Ollama.
    This list updates dynamically based on the models currently installed.
    """
    try:
        models = await fetch_models()
        return {"available_models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/message/")
async def send_message(request: ChatRequest):
    """
    Sends a message to the selected model and returns the response.

    Args:
        request (ChatRequest): JSON payload containing `model_name` and `user_message`.

    Returns:
        dict: The AI-generated response.
    """
    model_name = request.model_name
    user_message = request.user_message

    # Validate the model name
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found. Available models: {models}",
        )

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Prepare conversation context
    prompt = "\n".join(
        [
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in conversation_history
        ]
    )

    # Generate AI response
    response_chunks = []
    try:
        async for chunk in async_chat_with_model(model_name, prompt):
            response_chunks.append(chunk)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI model error: {str(e)}")

    # Store AI response in conversation history
    ai_response = "".join(response_chunks)
    conversation_history.append({"role": "ai", "content": ai_response})

    return {"message": ai_response}


@router.post("/message_sse/")
async def send_message_sse(request: ChatRequest):
    """
    Sends a message to the selected model and returns the response via SSE streaming.

    Args:
        request (ChatRequest): JSON payload containing `model_name` and `user_message`.

    Returns:
        StreamingResponse: Real-time AI response in chunks.
    """
    model_name = request.model_name
    user_message = request.user_message

    # Validate the model name
    models = await fetch_models()
    if model_name not in models:
        raise HTTPException(
            status_code=400,
            detail=f"Model '{model_name}' not found. Available models: {models}",
        )

    # Append user message to conversation history
    conversation_history.append({"role": "user", "content": user_message})

    # Prepare conversation context
    prompt = "\n".join(
        [
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in conversation_history
        ]
    )

    async def event_generator():
        """
        Generator function to stream AI response in real-time using SSE format.
        """
        try:
            async for chunk in async_chat_with_model(model_name, prompt):
                yield f"data: {chunk}\n\n"
        except Exception as e:
            yield f"data: [ERROR] {str(e)}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


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
