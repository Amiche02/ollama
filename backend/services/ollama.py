"""
Provides functions to interact with the Ollama API using async streaming via httpx.
"""

import json

import httpx  # Using httpx for async streaming
from config.config import OLLAMA_CHAT_URL, OLLAMA_MODELS_URL


async def fetch_models():
    """
    Asynchronously fetch the list of available models from Ollama.

    Returns:
        list[str]: A list of model names dynamically available in Ollama.
    """
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.get(OLLAMA_MODELS_URL)
            response.raise_for_status()
    except httpx.RequestError as e:
        raise ConnectionError(f"Error fetching models from Ollama: {e}")

    data = response.json()
    return [model["name"] for model in data.get("models", [])]


async def async_chat_with_model(model_name: str, prompt: str):
    """
    Send a chat request to Ollama with streaming enabled (async).

    Args:
        model_name (str): The name of the model to use (must exist in Ollama).
        prompt (str): The conversation or instructions.

    Yields:
        str: The response text (no fixed chunk size). Each yielded piece
             is one portion of Ollama's streaming response.
    """
    payload = {"model": model_name, "prompt": prompt, "stream": True}
    headers = {"Content-Type": "application/json"}

    try:
        async with httpx.AsyncClient(timeout=60) as client:
            async with client.stream(
                "POST", OLLAMA_CHAT_URL, json=payload, headers=headers
            ) as resp:
                resp.raise_for_status()
                async for line in resp.aiter_lines():
                    # Each line from Ollama should be a JSON object with {"response": "..."}
                    if not line.strip():
                        continue
                    try:
                        data = json.loads(line)
                        yield data.get("response", "")
                    except json.JSONDecodeError:
                        # Malformed line - skip
                        continue
    except httpx.RequestError as e:
        raise ConnectionError(f"Error connecting to Ollama: {e}")
