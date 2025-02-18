import os

import gradio as gr
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# -------------------------------------------------------------------
# Helper functions to interact with the backend
# -------------------------------------------------------------------


def list_all_docs():
    """
    Returns a list of all documents in the 'uploads/' folder
    by calling GET /docs/list.
    """
    try:
        resp = requests.get(f"{BACKEND_URL}/docs/list", timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("documents", [])
    except Exception as e:
        raise RuntimeError(f"Error listing documents: {e}")


def list_vectorized_docs():
    """
    Returns a list of vectorized (indexed) documents
    by calling GET /chromadb/list.

    We assume the backend endpoint returns something like:
       {"extracted_files": ["file1.pdf", "file2.txt", ...]}

    Adjust if your Chroma route is different.
    """
    try:
        resp = requests.get(f"{BACKEND_URL}/chromadb/list", timeout=30)
        resp.raise_for_status()
        data = resp.json()
        return data.get("extracted_files", [])
    except Exception as e:
        raise RuntimeError(f"Error listing vectorized docs: {e}")


def upload_documents(files):
    """
    Upload multiple documents to /docs/upload.
    Returns a status string for each file.
    """
    results = []
    for file in files:
        # Accept only pdf, txt, md, etc.
        # If you want to enforce it at the front-end level only:
        if not (
            file.name.lower().endswith(".pdf")
            or file.name.lower().endswith(".txt")
            or file.name.lower().endswith(".md")
        ):
            results.append(f"{file.name}: ❌ Invalid format.")
            continue

        try:
            files_param = {
                "files": (file.name, file, file.type or "application/octet-stream")
            }
            resp = requests.post(
                f"{BACKEND_URL}/docs/upload", files=files_param, timeout=60
            )
            resp.raise_for_status()
            data = resp.json()
            results.append(f"{file.name}: ✅ {data}")
        except Exception as e:
            results.append(f"{file.name}: ❌ Error: {str(e)}")
    return "\n".join(results)


def vectorize_documents(docs_to_vectorize):
    """
    Calls POST /text-extraction/extract_and_store with a list of filenames
    to embed them in Chroma.

    Body format:
      {"filenames": ["doc1.pdf", "doc2.txt", ...]}
    """
    if not docs_to_vectorize:
        return "No documents selected to vectorize."
    try:
        payload = {"filenames": docs_to_vectorize}
        resp = requests.post(
            f"{BACKEND_URL}/text-extraction/extract_and_store",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        data = resp.json()
        return f"Vectorization done:\n{data}"
    except Exception as e:
        return f"Error while vectorizing: {str(e)}"


def delete_document(filename):
    """
    Deletes a document from local disk ( /docs/delete/{filename} )
    and also tries to remove from Chroma ( /chromadb/delete/{filename} )
    so that doc + vectors are both removed.
    """
    if not filename:
        return "No filename provided."
    # 1) Delete the doc from /docs
    try:
        resp = requests.delete(f"{BACKEND_URL}/docs/delete/{filename}", timeout=30)
        resp.raise_for_status()
        doc_msg = resp.json()
    except Exception as e:
        return f"Failed to delete doc {filename}: {str(e)}"

    # 2) Delete from Chroma
    try:
        resp = requests.delete(f"{BACKEND_URL}/chromadb/delete/{filename}", timeout=30)
        resp.raise_for_status()
        vector_msg = resp.json()
    except Exception as e:
        return f"Document removed locally, but could not remove vectors: {str(e)}"

    return f"✅ {doc_msg}\n✅ {vector_msg}"


def get_personality_prompts():
    """
    If you want to dynamically fetch the personality list from the backend,
    you could do so. Otherwise, return a static list.
    """
    return [
        "Universal",
        "Casual",
        "DeepThinker",
        "KnowledgeNavigator",
        "Investigator",
        "Facilitator",
    ]


def chat_with_backend(model_name, personality, user_message, use_web, use_rag):
    """
    Send a chat request to /chat/message
    Return the text response. We'll display it as markdown in Gradio.
    """
    if not user_message.strip():
        return "⚠️ Please type a message."

    payload = {
        "model_name": model_name,
        "user_message": user_message,
        "personality": personality,
        "use_web_search": use_web,
        "use_rag": use_rag,
        "stream": False,  # if you want streaming, you'd implement differently
    }
    try:
        resp = requests.post(f"{BACKEND_URL}/chat/message", json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        return data.get("message", "No response from AI.")
    except Exception as e:
        return f"❌ Error from backend: {str(e)}"


# -------------------------------------------------------------------
#  Gradio Interface
# -------------------------------------------------------------------


def build_ui():
    with gr.Blocks() as demo:
        gr.Markdown("# RAG Backend - Gradio UI")

        with gr.Tab("Document Management"):
            gr.Markdown("## Manage Documents")
            with gr.Row():
                file_uploader = gr.File(
                    label="Upload Documents (PDF, TXT, MD only)",
                    file_count="multiple",
                    type="file",
                )
                upload_button = gr.Button("Upload")
            upload_results = gr.Textbox(label="Upload Results", interactive=False)

            gr.Markdown("### Vectorization")
            with gr.Row():
                refresh_docs_button = gr.Button("Refresh Doc List")
                vectorize_button = gr.Button("Vectorize Selected Documents")
            docs_status = gr.Textbox(label="Status", interactive=False, lines=5)

            # We'll show two checklists: non-vectorized & vectorized
            non_vectorized_list = gr.CheckboxGroup(
                choices=[], label="Non-Vectorized Documents"
            )
            vectorized_list = gr.CheckboxGroup(choices=[], label="Vectorized Documents")
            delete_button = gr.Button("Delete Selected Docs")

            # -- define interactions for document management
            def on_upload(files):
                return upload_documents(files)

            upload_button.click(
                fn=on_upload, inputs=[file_uploader], outputs=[upload_results]
            )

            def refresh_docs():
                try:
                    all_docs = list_all_docs()
                    vec_docs = list_vectorized_docs()
                    not_vec = sorted(set(all_docs) - set(vec_docs))
                    return (
                        gr.update(choices=not_vec, value=[]),
                        gr.update(choices=vec_docs, value=[]),
                        "Lists refreshed.",
                    )
                except Exception as e:
                    return gr.update(), gr.update(), f"Error: {str(e)}"

            refresh_docs_button.click(
                fn=refresh_docs,
                inputs=[],
                outputs=[non_vectorized_list, vectorized_list, docs_status],
            )

            def do_vectorize(selected_docs):
                if not selected_docs:
                    return "No documents selected."
                result = vectorize_documents(selected_docs)
                return result

            vectorize_button.click(
                fn=do_vectorize, inputs=[non_vectorized_list], outputs=[docs_status]
            )

            def do_delete(selected_non_vec, selected_vec):
                # We'll delete from whichever list they're in
                # Combined = selected_non_vec + selected_vec
                if not (selected_non_vec or selected_vec):
                    return "No documents selected."
                combined = list(set(selected_non_vec + selected_vec))

                msgs = []
                for doc in combined:
                    msgs.append(delete_document(doc))
                return "\n\n".join(msgs)

            delete_button.click(
                fn=do_delete,
                inputs=[non_vectorized_list, vectorized_list],
                outputs=[docs_status],
            )

        with gr.Tab("Chat"):
            gr.Markdown("## Chat with the AI")
            with gr.Row():
                model_input = gr.Textbox(label="Model name", value="all-MiniLM-L12-v2")
                personality_dropdown = gr.Dropdown(
                    label="Personality Prompt",
                    choices=get_personality_prompts(),
                    value="Universal",
                )
            with gr.Row():
                use_websearch_checkbox = gr.Checkbox(
                    label="Use Web Search?", value=False
                )
                use_rag_checkbox = gr.Checkbox(
                    label="Use Document Retrieval?", value=False
                )

            user_message = gr.Textbox(
                label="Your Message", lines=3, placeholder="Type something..."
            )
            chat_button = gr.Button("Send Message")
            chat_output = gr.Markdown(label="AI Response")

            def on_chat(model, pers, msg, w_search, rag):
                return chat_with_backend(model, pers, msg, w_search, rag)

            chat_button.click(
                fn=on_chat,
                inputs=[
                    model_input,
                    personality_dropdown,
                    user_message,
                    use_websearch_checkbox,
                    use_rag_checkbox,
                ],
                outputs=chat_output,
            )

    return demo


if __name__ == "__main__":
    # Launch the Gradio app
    ui = build_ui()
    ui.launch(server_name="127.0.0.1", server_port=7860)
