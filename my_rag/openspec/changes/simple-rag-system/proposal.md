## Why

Building a local RAG (Retrieval-Augmented Generation) system as a learning project to understand how document retrieval, embeddings, vector databases, and LLMs work together. This is a standalone educational project (not related to the capstone) that uses entirely local models to avoid API costs and provide full control over the system.

## What Changes

- Create a complete RAG pipeline with local embeddings (sentence-transformers), vector storage (ChromaDB), and local LLM (Ollama with Llama 3.1 8B)
- Build document ingestion system supporting PDF, TXT, and Markdown files with intelligent chunking
- Implement semantic search and retrieval with top-k similarity matching
- Create a vibrant, modern web UI using Streamlit with gradient backgrounds, smooth animations, dark/light mode toggle, and colorful accents
- Provide CLI tools for document ingestion and querying
- Structure implementation in clear phases for progressive learning

## Capabilities

### New Capabilities
- `document-ingestion`: Load, parse, chunk, and embed documents (PDF/TXT/MD) into vector database
- `vector-search`: Semantic search over embedded documents using similarity matching
- `llm-generation`: Generate contextual responses using retrieved chunks and local Ollama LLM
- `web-ui`: Interactive Streamlit interface with vibrant theme, animations, and dark/light modes

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

- New Python project structure with modular components (embedder, vector store, retriever, LLM interface)
- Dependencies: sentence-transformers, chromadb, ollama, streamlit, pypdf, rich
- Requires Ollama installation and Llama 3.1 8B model (~5GB download)
- Local storage for ChromaDB vector database (~100MB-1GB depending on document corpus)
- System requirements: 8GB+ RAM recommended, optional GPU for faster inference
