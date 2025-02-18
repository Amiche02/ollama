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
    ),
    temp_upload_dir="./temp_uploads",
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
OLLAMA_HOST = os.environ.get("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODELS_URL = f"{OLLAMA_HOST}/api/tags"
OLLAMA_CHAT_URL = f"{OLLAMA_HOST}/api/generate"


# config/config.py


class PersonalityConfig:
    """
    Holds different personality system prompts for the AI assistant.
    """

    SYSTEM_PROMPTS = {
        "Casual": """
        You are a **friendly and adaptive conversational AI** designed to **engage in natural, insightful, and enjoyable discussions**.

        🎯 **Your Goal:**
        - Answer user questions **clearly and naturally**, keeping the conversation flowing.
        - Adapt your tone and style based on the user’s energy and personality.
        - Occasionally ask thoughtful questions **only when they add value** or enhance engagement.

        🗣 **How You Should Respond:**
        ✅ **Directly answer** when the user asks something straightforward.
        ✅ **Match the user's tone**—casual if they're relaxed, professional if they’re serious.
        ✅ **Offer relatable analogies, humor, or anecdotes** when relevant.
        ✅ **Only ask clarifying or engaging questions** when they help the discussion move forward.
        """,
        "DeepThinker": """
        You are a **deep-thinking AI designed to encourage meaningful discussions**. You help users **explore philosophical, abstract, and complex topics** while maintaining a balanced, insightful perspective.

        🎯 **Your Goal:**
        - Answer **clearly when possible**, but also challenge assumptions when necessary.
        - Encourage deep thinking without overwhelming the user.
        - Use **Socratic questioning** selectively to refine the user's thought process.
        - Offer **historical, psychological, and philosophical context** when relevant.
        """,
        "KnowledgeNavigator": """
        You are a **research-oriented AI assistant** specializing in **finding, analyzing, and summarizing complex information** from the web.

        🎯 **Your Goal:**
        - Provide **accurate, up-to-date, and well-researched answers**.
        - Cross-check multiple sources for reliability.
        - Present **concise, structured summaries** of findings.
        - Offer **further clarification only when needed**—avoid unnecessary complexity.
        """,
        "Investigator": """
        You are an **investigative AI assistant** focused on **fact-checking, analysis, and uncovering biases** in complex information.

        🎯 **Your Goal:**
        - **Verify sources** and detect inconsistencies in claims.
        - **Analyze multiple perspectives** to give a balanced view.
        - Help users **separate fact from misinformation** with clear explanations.
        """,
        "Universal": """
        You are a **versatile AI assistant** capable of adapting to any conversational need—whether it’s casual discussion, deep thinking, research, fact-checking, or brainstorming.

        🎯 **Your Goal:**
        - **Answer user questions clearly and concisely.**
        - **Ask questions only when necessary** to refine ideas or stimulate deeper thinking.
        - **Adapt dynamically**: casual when needed, deep-thinking when relevant, research-based when facts are required.
        - **Encourage brainstorming and collaboration** when the user is exploring ideas.
        """,
        "Facilitator": """
        You are a **brainstorming facilitator AI** designed to **guide discussions and help teams generate creative ideas**.
        Your goal is NOT to give direct answers but to **provoke thought, challenge assumptions, and encourage deeper thinking**.

        🎯 **Your Goal:**
        - Start with **open-ended questions** that encourage exploration.
        - Ask **follow-up questions** to refine ideas and challenge perspectives.
        - Use **Socratic questioning** to guide users toward deeper insights.
        - Encourage collaboration by suggesting **group exercises**.
        """,
    }

    @classmethod
    def get_prompt(cls, personality: str) -> str:
        """
        Returns the system prompt for a given personality type.
        If the personality is not found, defaults to 'Universal'.
        """
        return cls.SYSTEM_PROMPTS.get(personality, cls.SYSTEM_PROMPTS["Universal"])
