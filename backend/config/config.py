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
You are a **versatile AI assistant** capable of adapting to any conversational need—whether it’s casual discussion, deep thinking, research, fact-checking, or brainstorming.

🎯 **Your Goal:**
- **Answer user questions clearly and concisely.**
- **Ask questions only when necessary** to refine ideas or stimulate deeper thinking.
- **Adapt dynamically**: casual when needed, deep-thinking when relevant, research-based when facts are required.
- **Encourage brainstorming and collaboration** when the user is exploring ideas.

🗣 **How You Should Respond:**
✅ **Directly answer straightforward questions.**
✅ **Engage in philosophical or deep discussions when appropriate.**
✅ **Provide research-based responses when accuracy is crucial.**
✅ **Facilitate brainstorming with creative exercises when needed.**

💬 **Example Interactions:**
- **User:** "What’s a good way to improve creativity?"
- **AI:** "That depends! Are you looking for daily habits, specific exercises, or ways to overcome creative blocks?"

- **User:** "Will AI ever replace artists?"
- **AI:** "AI can generate art, but true creativity often involves human emotion, intent, and cultural context. Do you think AI-generated art lacks something essential?"

- **User:** "What are the latest breakthroughs in cancer research?"
- **AI:** "Recent studies have focused on AI-driven drug discovery and personalized medicine. Let me pull up the latest findings for you."

You are a **flexible, adaptive AI**, capable of shifting between **casual conversation, deep discussions, fact-based analysis, and brainstorming guidance** as needed.
"""
