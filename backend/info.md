# API Reference: Curl Commands for Backend Interaction

This document provides a comprehensive list of `curl` commands to interact with the backend API.

---

## 📌 **General Routes**

### ✅ **Health Check**
```sh
curl -X GET "http://127.0.0.1:8000/health"
```

---

## 📂 **ChromaDB Routes**

### 🔍 **List Indexed Documents**
```sh
curl -X GET "http://127.0.0.1:8000/chromadb/list/"
```

### 🔎 **Query ChromaDB**
```sh
curl -X POST "http://127.0.0.1:8000/chromadb/query/" \
     -H "Content-Type: application/json" \
     -d '{"query": "your query text"}'
```

### 🗑 **Delete Specific Document from ChromaDB**
```sh
curl -X DELETE "http://127.0.0.1:8000/chromadb/delete/{filename}"
```

### 🚀 **Clear All ChromaDB Data**
```sh
curl -X DELETE "http://127.0.0.1:8000/chromadb/clear/"
```

### 📄 **Retrieve Extracted Text from a Document**
```sh
curl -X GET "http://127.0.0.1:8000/chromadb/get/{filename}"
```

---

## 📁 **File Management Routes**

### 📤 **Upload Documents**
```sh
curl -X POST "http://127.0.0.1:8000/docs/upload/" \
     -F "files=@/path/to/your/file1.pdf" \
     -F "files=@/path/to/your/file2.txt"
```

### 📂 **List Uploaded Documents**
```sh
curl -X GET "http://127.0.0.1:8000/docs/list/"
```

### ❌ **Delete a Specific Document**
```sh
curl -X DELETE "http://127.0.0.1:8000/docs/delete/{filename}"
```

---

## 📝 **Text Extraction Routes**

### 📑 **Extract and Store Text in ChromaDB**
```sh
curl -X POST "http://127.0.0.1:8000/text-extraction/extract_and_store/" \
     -H "Content-Type: application/json" \
     -d '{"filenames": ["document1.pdf", "notes.md"]}'
```

---

## 🌍 **Web Search Routes**

### 🔎 **Perform Web Search and Index Results**
```sh
curl -X POST "http://127.0.0.1:8000/websearch/search/" \
     -H "Content-Type: application/json" \
     -d '{"query": "your search query", "max_results": 5}'
```

---

## 🤖 **Chatbot Routes**

### 🤖 **List Available AI Models**
```sh
curl -X GET "http://127.0.0.1:8000/chat/available_models/"
```

### 🗂 **Get Chat History**
```sh
curl -X GET "http://127.0.0.1:8000/chat/history/"
```

### 🗑 **Clear Chat History**
```sh
curl -X DELETE "http://127.0.0.1:8000/chat/clear_history/"
```

---

## 🔥 **New Features & Functionalities**

✔ **Web Search (`use_web_search`)**: Queries external sources (DuckDuckGo) and includes relevant snippets.
✔ **RAG (`use_rag`)**: Searches ChromaDB for relevant documents and includes them in the prompt.
✔ **Streaming Mode (`stream`)**: AI responses are streamed in real-time using SSE.
✔ **Adaptive AI Personality**: The model adapts based on predefined personalities (`Casual`, `Deep Thinker`, `Knowledge Navigator`, etc.).

---

## 📌 **Example Requests**

### **1️⃣ Enable Web Search and RAG with Streaming**
```bash
curl -X POST "http://127.0.0.1:8000/chat/message/" \
     -H "Content-Type: application/json" \
     -d '{
           "model_name": "deepseek-r1",
           "user_message": "What are the latest advancements in AI?",
           "use_web_search": true,
           "use_rag": true,
           "stream": true
         }'
```

### **2️⃣ Only Web Search (No Streaming)**
```bash
curl -X POST "http://127.0.0.1:8000/chat/message/" \
     -H "Content-Type: application/json" \
     -d '{
           "model_name": "deepseek-r1",
           "user_message": "What are the best DevOps practices?",
           "use_web_search": true,
           "use_rag": false,
           "stream": false
         }'
```

### **3️⃣ Only RAG (No Streaming)**
```bash
curl -X POST "http://127.0.0.1:8000/chat/message/" \
     -H "Content-Type: application/json" \
     -d '{
           "model_name": "deepseek-r1",
           "user_message": "Explain Kubernetes architecture.",
           "use_web_search": false,
           "use_rag": true,
           "stream": false
         }'
```

### **4️⃣ Neither Web Search nor RAG (Direct Response)**
```bash
curl -X POST "http://127.0.0.1:8000/chat/message/" \
     -H "Content-Type: application/json" \
     -d '{
           "model_name": "deepseek-r1",
           "user_message": "Tell me about black holes.",
           "use_web_search": false,
           "use_rag": false,
           "stream": false
         }'
```

---

## 🎯 **Conclusion**

This guide provides `curl` commands for all major API interactions, including AI chatbot messaging, document processing, ChromaDB management, and web search functionalities. Whether you're debugging or integrating, this reference should streamline your workflow!

🚀 **Happy coding!**
