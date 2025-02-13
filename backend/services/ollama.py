"""
Provides functions to interact with the Ollama API.
"""

import json

import requests
from config.config import OLLAMA_CHAT_URL, OLLAMA_MODELS_URL


def fetch_models():
    """
    Fetch the list of available models from Ollama.

    Returns:
        list[str]: A list of model names.
    """
    try:
        # Add timeout to address B113
        response = requests.get(OLLAMA_MODELS_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ConnectionError(f"Error fetching models from Ollama: {e}")

    data = response.json()
    models = [model["name"] for model in data.get("models", [])]
    return models


def chat_with_model(model_name, prompt):
    """
    Send a chat request to Ollama with streaming enabled.

    Args:
        model_name (str): The name of the model to use.
        prompt (str): The conversation history (system + user messages).

    Yields:
        str: The response text as it is streamed from Ollama.
    """
    payload = {"model": model_name, "prompt": prompt, "stream": True}
    headers = {"Content-Type": "application/json"}

    try:
        # Add timeout to address B113
        with requests.post(
            OLLAMA_CHAT_URL, json=payload, headers=headers, stream=True, timeout=10
        ) as r:
            r.raise_for_status()

            # Reading the response line by line.
            for line in r.iter_lines(decode_unicode=True):
                if line:  # Non-empty line
                    try:
                        data = json.loads(line)
                        # Each line should be a JSON object with {"response": "..."}
                        yield data.get("response", "")
                    except json.JSONDecodeError:
                        # In case there's any malformed line, we skip or handle it
                        pass

    except requests.RequestException as e:
        raise ConnectionError(f"Error connecting to Ollama: {e}")
