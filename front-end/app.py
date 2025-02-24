import os
import re

import requests
import streamlit as st
from streamlit_chat import message

# ---------------------------
#          BACKEND URLs
# ---------------------------
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")  # For Docker usage
CHAT_ENDPOINT = f"{BACKEND_URL}/chat/message/"
MODELS_ENDPOINT = f"{BACKEND_URL}/chat/available_models/"
DOCS_LIST_ENDPOINT = f"{BACKEND_URL}/docs/list/"
UPLOAD_DOC_ENDPOINT = f"{BACKEND_URL}/docs/upload/"
BUILD_VECTOR_ENDPOINT = f"{BACKEND_URL}/text-extraction/extract_and_store/"


# ---------------------------
#       HELPER FUNCTIONS
# ---------------------------
def separate_think_from_answer(text: str):
    """
    Splits 'text' into (chain_of_thought, final_answer).
    If <think> is not found, returns ("", text).
    """
    pattern = r"<think>(.*?)</think>"
    match = re.search(pattern, text, flags=re.DOTALL)
    if match:
        chain_of_thought = match.group(1).strip()
        # Remove entire <think>...</think> block from the text
        final_answer = re.sub(pattern, "", text, flags=re.DOTALL).strip()
        return chain_of_thought, final_answer
    else:
        # No <think> block
        return "", text


def handle_streaming_response(resp):
    """
    Reads chunked lines from 'resp' (requests.Response with stream=True),
    accumulates them into partial_markdown, and displays partial updates
    with st.markdown, while also checking for <think> blocks.
    """
    partial_markdown = ""
    stream_container = st.empty()

    for chunk in resp.iter_lines():
        if chunk:
            chunk_text = chunk.decode("utf-8", errors="ignore")
            # Remove leading "data: " if present
            if chunk_text.startswith("data: "):
                chunk_text = chunk_text[len("data: ") :]

            # Accumulate chunk text
            partial_markdown += chunk_text
            # Live-update with markdown
            stream_container.markdown(partial_markdown)

    # At the end, separate chain-of-thought from final
    chain_of_thought, final_answer = separate_think_from_answer(partial_markdown)
    return chain_of_thought, final_answer


# ---------------------------
#         PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="RAG + Web Search Chatbot", layout="wide")
st.title("AI Chatbot with RAG & Web Search")

# ---------------------------
#         SIDEBAR
# ---------------------------
st.sidebar.header("Configuration")

# 1) Document Management
st.sidebar.subheader("Document Management")
uploaded_files = st.sidebar.file_uploader(
    "Upload documents",
    accept_multiple_files=True,
    type=["pdf", "txt", "md", "html"],
    help="Select one or more documents to upload",
)
if st.sidebar.button("Upload Documents"):
    if uploaded_files:
        files_to_upload = []
        for upf in uploaded_files:
            file_bytes = upf.read()
            files_to_upload.append(
                ("files", (upf.name, file_bytes, "application/octet-stream"))
            )
        try:
            resp = requests.post(UPLOAD_DOC_ENDPOINT, files=files_to_upload, timeout=60)
            if resp.status_code == 200:
                st.sidebar.success("Documents uploaded successfully!")
            else:
                st.sidebar.error(f"Upload failed: {resp.text}")
        except Exception as e:
            st.sidebar.error(f"Upload error: {e}")
    else:
        st.sidebar.warning("No files selected.")

# 2) Existing Documents
st.sidebar.write("---")
st.sidebar.subheader("Existing Documents")
try:
    docs_list_resp = requests.get(DOCS_LIST_ENDPOINT, timeout=10)
    if docs_list_resp.status_code == 200:
        document_options = docs_list_resp.json().get("documents", [])
    else:
        st.sidebar.error(f"Error listing docs: {docs_list_resp.text}")
        document_options = []
except Exception as e:
    st.sidebar.error(f"Could not fetch documents: {e}")
    document_options = []

if document_options:
    st.sidebar.write("Available documents:")
    for doc in document_options:
        st.sidebar.write(f"- {doc}")

# 3) Build Vector Base
if document_options:
    st.sidebar.write("---")
    st.sidebar.subheader("Build Vector Base")
    selected_docs = st.sidebar.multiselect(
        "Select docs for indexing:", document_options
    )
    if st.sidebar.button("Index Documents"):
        if selected_docs:
            try:
                payload = {"filenames": selected_docs}
                index_resp = requests.post(
                    BUILD_VECTOR_ENDPOINT, json=payload, timeout=500
                )
                if index_resp.status_code == 200:
                    st.sidebar.success("Vector DB updated successfully!")
                else:
                    st.sidebar.error(f"Vectorization failed: {index_resp.text}")
            except Exception as e:
                st.sidebar.error(f"Indexing error: {e}")
        else:
            st.sidebar.warning("No documents selected for indexing.")

# 4) Model & Personality
st.sidebar.write("---")
st.sidebar.subheader("Model Settings")
try:
    models_resp = requests.get(MODELS_ENDPOINT, timeout=10)
    if models_resp.status_code == 200:
        available_models = models_resp.json().get("models", [])
    else:
        st.sidebar.error(f"Could not fetch models: {models_resp.text}")
        available_models = []
except Exception as e:
    st.sidebar.error(f"Error fetching models: {e}")
    available_models = []

if not available_models:
    available_models = ["llama3.2:latest"]  # fallback

selected_model = st.sidebar.selectbox("Choose AI Model:", options=available_models)

personality_options = [
    "Casual",
    "DeepThinker",
    "KnowledgeNavigator",
    "Investigator",
    "Universal",
    "Facilitator",
]
selected_personality = st.sidebar.selectbox("Choose Personality:", personality_options)

# 5) Retrieval & Streaming
st.sidebar.write("---")
st.sidebar.subheader("Retrieval & Streaming")
use_rag = st.sidebar.checkbox("Enable RAG (Vector Search)", value=True)
use_web_search = st.sidebar.checkbox("Enable Web Search", value=False)
stream_response = st.sidebar.checkbox("Enable Streaming Mode", value=False)

# ---------------------------
#         MAIN CHAT
# ---------------------------
st.write("Chat with your AI assistant below. Use RAG/WebSearch for smarter responses.")

# Keep chat history in session_state
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Display existing conversation
for i, chat_msg in enumerate(st.session_state["chat_history"]):
    role = chat_msg["role"]
    # We'll store chain_of_thought separately if you want
    chain_of_thought = chat_msg.get("thought", "")
    content = chat_msg["content"]

    if chain_of_thought:
        # Optionally show chain_of_thought behind an expander
        with st.expander(f"Chain-of-thought (hidden) for message {i}"):
            st.markdown(f"```\n{chain_of_thought}\n```")

    message(content, is_user=(role == "user"), key=f"chat_{i}")

st.write("---")
user_input = st.text_input("Enter your message:", "")

# Single-message web search toggle
single_search_toggle = st.checkbox("Web Search only for this query?")

# Send logic
if st.button("Send"):
    if not user_input.strip():
        st.warning("Please enter a message.")
    else:
        # Add user message
        st.session_state["chat_history"].append({"role": "user", "content": user_input})

        payload = {
            "model_name": selected_model,
            "user_message": user_input,
            "personality": selected_personality,
            "use_web_search": (single_search_toggle or use_web_search),
            "use_rag": use_rag,
            "stream": stream_response,
        }

        try:
            with requests.post(
                CHAT_ENDPOINT, json=payload, stream=stream_response, timeout=300
            ) as resp:
                if resp.status_code == 200:
                    if stream_response:
                        # SSE or chunked text => streaming
                        chain_of_thought, final_answer = handle_streaming_response(resp)
                        # Save final to chat
                        st.session_state["chat_history"].append(
                            {
                                "role": "ai",
                                "content": final_answer,
                                "thought": chain_of_thought,
                            }
                        )
                    else:
                        # Non-stream => final JSON
                        data = resp.json()
                        raw_ai_response = data.get("message", "")

                        # separate <think> from the final
                        chain_of_thought, final_answer = separate_think_from_answer(
                            raw_ai_response
                        )

                        # Show sources
                        if "sources" in data:
                            with st.expander("Sources & References"):
                                st.json(data["sources"])

                        # Add to chat
                        st.session_state["chat_history"].append(
                            {
                                "role": "ai",
                                "content": final_answer,
                                "thought": chain_of_thought,
                            }
                        )
                else:
                    error_msg = f"AI Error: {resp.text}"
                    st.session_state["chat_history"].append(
                        {"role": "ai", "content": error_msg}
                    )
        except Exception as e:
            st.session_state["chat_history"].append(
                {"role": "ai", "content": f"Exception: {e}"}
            )

        st.rerun()

# Clear Chat Button
if st.button("Clear Conversation"):
    st.session_state["chat_history"].clear()
    st.rerun()
