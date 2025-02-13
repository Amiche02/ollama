import pytest
from services.ollama import chat_with_model, fetch_models


@pytest.mark.skip(reason="Requires a running Ollama server on localhost:11434")
def test_fetch_models():
    models = fetch_models()
    # Marking assert with # nosec B101 to silence Bandit about production asserts
    assert isinstance(models, list), "Models should be returned as a list"  # nosec B101
    assert len(models) > 0, "Should have at least one model"  # nosec B101


@pytest.mark.skip(reason="Requires a running Ollama server on localhost:11434")
def test_chat_with_model():
    # This test requires a valid model name and running Ollama server.
    models = fetch_models()
    first_model = models[0]

    prompt = "System: Hello\nUser: Hello"
    responses = list(chat_with_model(first_model, prompt))
    # Marking assert with # nosec B101 to silence Bandit about production asserts
    assert len(responses) > 0, "Should receive some streamed response"  # nosec B101
