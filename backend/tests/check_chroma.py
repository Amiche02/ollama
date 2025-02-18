import chromadb

# Connect to ChromaDB (ensure the path is correct)
client = chromadb.PersistentClient(
    path="/home/amiche/Documents/JUNIA/DEVOPS/ollama/backend/chroma_db"
)

# Get ChromaDB collection
collection_name = "rag_collection"  # Adjust to match your setup
collection = client.get_collection(collection_name)

# Fetch all stored documents
results = collection.get(include=["documents", "metadatas"])

# Print stored documents
print("\n📂 **Indexed Documents in ChromaDB:**")
for i, doc in enumerate(results.get("documents", [])):
    print(f"📝 Document {i+1}: {doc[:500]}...")  # Print first 500 chars

print("\n🔖 **Metadata:**")
for i, meta in enumerate(results.get("metadatas", [])):
    print(f"ℹ️ Metadata {i+1}: {meta}")
