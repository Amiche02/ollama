"""
Configuration constants or environment variables for the Ollama application.
"""

import os
from typing import List, Optional

from pydantic import BaseModel, Field


class EmbeddingModelConfig(BaseModel):
    name: str
    language: Optional[List[str]] = None
    model_path: str
    description: Optional[str] = None


class FileTypeConfig(BaseModel):
    supported_extensions: List[str]
    extraction_methods: dict


class TextExtractorConfig(BaseModel):
    extraction_settings: FileTypeConfig
    temp_upload_dir: str = Field(
        "./temp_uploads", description="Directory to store temporary file uploads."
    )


# Configuration for text extraction
TEXT_EXTRACTOR_CONFIG = TextExtractorConfig(
    extraction_settings=FileTypeConfig(
        supported_extensions=["pdf", "txt", "md", "html"],
        extraction_methods={
            "pdf": "extract_text_from_pdf",
            "txt": "extract_text_from_text",
            "md": "extract_text_from_text",
            "html": "extract_text_from_html",
        },
    )
)

# Define available embedding models
AVAILABLE_EMBEDDING_MODELS = [
    {
        "name": "paraphrase-multilingual-MiniLM-L12-v2",
        "language": ["en", "fr", "it", "es", "de", "zh", "ja", "ru", "ar"],
        "model_path": "paraphrase-multilingual-MiniLM-L12-v2",
        "description": "A multilingual model supporting multiple languages.",
    },
    {
        "name": "all-MiniLM-L12-v2",
        "language": ["en"],
        "model_path": "all-MiniLM-L12-v2",
        "description": "An English-only model optimized for speed and accuracy.",
    },
]

# You can set these via environment variables or just hardcode them.
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODELS_URL = f"{OLLAMA_HOST}/api/tags"
OLLAMA_CHAT_URL = f"{OLLAMA_HOST}/api/generate"

# System prompt for the brainstorming facilitator AI
SYSTEM_PROMPT = """
You are a **brainstorming facilitator AI** designed to **guide discussions and help teams generate creative ideas**.
Your goal is NOT to give direct answers but to **provoke thought, challenge assumptions, and encourage deeper thinking**.

**How you should respond:**
1️⃣ **Start with an open-ended question** that encourages exploration.
2️⃣ **Ask follow-up questions** to refine ideas and challenge perspectives.
3️⃣ **Use Socratic questioning** to guide users toward deeper insights.
4️⃣ **Encourage collaboration** by suggesting group exercises.
5️⃣ **Summarize key points** occasionally to keep the discussion structured.

**Tone & Style:**
✅ Encouraging, positive, and engaging.
✅ Adaptive: If the user seems stuck, offer **alternative ways to explore the topic**.
✅ Do not provide direct answers—help the user **think for themselves**.

💡 Example Interaction:
- **User:** "I need an innovative idea for a startup."
- **AI:** "Great! What industry excites you the most? Do you want to solve a specific problem?"
- **User:** "Something related to AI and education."
- **AI:** "Interesting! How do you think AI could **personalize** learning experiences? What are some existing challenges in education that AI could solve?"

Remember: **Your role is to animate discussions, not to provide all the answers!**
"""
