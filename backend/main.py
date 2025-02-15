import uvicorn
from fastapi import FastAPI
from routes.chat import router as chat_router
from routes.chromadb import router as chromadb_router  # Ajout de ChromaDB
from routes.file_manager import router as file_manager_router
from routes.text_extraction import router as text_extraction_router
from routes.websearch import router as websearch_router

app = FastAPI()

# Register document management API
app.include_router(file_manager_router)
app.include_router(websearch_router)
app.include_router(text_extraction_router)
app.include_router(chat_router)
app.include_router(chromadb_router)


@app.get("/")
def home():
    return {"message": "Welcome to the RAG system!"}


@app.get("/health")
def health_check():
    """
    Vérifie si le backend tourne correctement.
    """
    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
