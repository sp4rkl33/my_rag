## 1. Project Setup

- [x] 1.1 Create project directory structure (src/, data/documents/, storage/chroma/)
- [x] 1.2 Create requirements.txt with dependencies (sentence-transformers, chromadb, ollama, streamlit, pypdf, rich, typer)
- [x] 1.3 Create README.md with setup instructions and system requirements
- [x] 1.4 Create .gitignore for Python project (exclude storage/, __pycache__, .env)

## 2. Phase 1 - Core RAG Pipeline (Embeddings & Vector Store)

- [x] 2.1 Implement src/embedder.py with SentenceTransformer wrapper for all-MiniLM-L6-v2
- [x] 2.2 Add batch embedding generation method to embedder
- [x] 2.3 Implement src/vectorstore.py with ChromaDB client initialization
- [x] 2.4 Add methods to store embeddings with metadata (text, source, chunk_index)
- [x] 2.5 Add method to check for duplicate documents before ingestion
- [x] 2.6 Implement src/retriever.py with query embedding and similarity search
- [x] 2.7 Add configurable top-k and similarity threshold parameters to retriever
- [x] 2.8 Add method to return results with metadata (source, score, chunk_index)
- [x] 2.9 Test core pipeline: embed sample text, store in ChromaDB, retrieve similar chunks

## 3. Phase 2 - LLM Integration (Ollama)

- [x] 3.1 Implement src/llm.py with Ollama client connection (localhost:11434)
- [x] 3.2 Add method to verify Ollama is running and accessible
- [x] 3.3 Add method to check if llama3.1:8b model is available
- [x] 3.4 Implement prompt construction method (system + context + query format)
- [x] 3.5 Add method to handle context truncation for token limits (8192 tokens)
- [x] 3.6 Implement streaming response generation with configurable temperature and max_tokens
- [x] 3.7 Add error handling for Ollama connection failures and generation errors
- [x] 3.8 Implement method to return response metadata (tokens, generation time, model)
- [x] 3.9 Test LLM integration: send prompt to Ollama and stream response

## 4. Phase 3 - Document Ingestion

- [x] 4.1 Implement src/parser.py with PDF text extraction using pypdf
- [x] 4.2 Add TXT and MD file parsing with UTF-8 encoding
- [x] 4.3 Add error handling for corrupted or unreadable files
- [x] 4.4 Implement src/chunker.py with fixed-size chunking (500-1000 tokens, 100 overlap)
- [x] 4.5 Add logic to split at sentence/paragraph boundaries when possible
- [x] 4.6 Add handling for documents smaller than chunk size (single chunk)
- [x] 4.7 Implement src/rag.py as main pipeline orchestrator
- [x] 4.8 Add method to ingest single file (parse → chunk → embed → store)
- [x] 4.9 Add method to ingest directory recursively (find all PDF/TXT/MD files)
- [x] 4.10 Add progress logging for batch ingestion
- [x] 4.11 Create ingest.py CLI script with typer for document ingestion
- [x] 4.12 Add --dir and --file arguments to ingest.py
- [x] 4.13 Test ingestion: load sample documents and verify in ChromaDB

## 5. RAG Query Pipeline

- [x] 5.1 Add query method to src/rag.py (embed query → retrieve → generate response)
- [x] 5.2 Add handling for empty database (no documents indexed)
- [x] 5.3 Add handling for no relevant results (below similarity threshold)
- [x] 5.4 Create query.py CLI script for testing queries from command line
- [x] 5.5 Test end-to-end RAG: ingest documents, ask questions, verify contextual answers

## 6. Phase 4 - Vibrant Web UI (Streamlit)

- [x] 6.1 Create app.py as main Streamlit application entry point
- [x] 6.2 Add custom CSS for gradient backgrounds (purple/blue/pink gradients)
- [x] 6.3 Add CSS for smooth transitions and animations on interactive elements
- [x] 6.4 Implement dark/light mode toggle with CSS variables
- [x] 6.5 Add session state management for theme preference
- [x] 6.6 Create sidebar with settings panel (top-k, similarity threshold, temperature, max_tokens)
- [x] 6.7 Implement document upload interface with file uploader widget
- [x] 6.8 Add progress indicators for file upload and ingestion
- [x] 6.9 Create document library section showing indexed documents and chunk count
- [x] 6.10 Add "Clear Database" button with confirmation dialog
- [x] 6.11 Implement main query interface with text input and submit button
- [x] 6.12 Add conversation history display (questions and answers)
- [x] 6.13 Implement streaming response display with typing animation effect
- [x] 6.14 Add markdown rendering for formatted responses
- [x] 6.15 Create expandable section for source citations (documents and chunks used)
- [x] 6.16 Display response metadata (generation time, token count, retrieval info)
- [x] 6.17 Add error handling UI for Ollama not running, empty database, generation failures
- [x] 6.18 Implement responsive design for desktop, tablet, and mobile layouts
- [ ] 6.19 Test UI on different screen sizes and browsers

## 7. Documentation & Polish

- [x] 7.1 Update README.md with complete setup instructions (Ollama installation, model pull)
- [x] 7.2 Add usage examples to README (CLI and web UI)
- [x] 7.3 Document system requirements (RAM, GPU optional, disk space)
- [x] 7.4 Add troubleshooting section to README (common errors and solutions)
- [x] 7.5 Create example documents directory with sample files for testing
- [x] 7.6 Add inline code comments for complex logic
- [ ] 7.7 Test complete workflow: setup → ingest → query via CLI → query via UI
- [ ] 7.8 Create screenshots of vibrant UI for README

## 8. Final Testing & Validation

- [ ] 8.1 Test with various document types (PDF, TXT, MD)
- [ ] 8.2 Test with large document corpus (100+ files)
- [ ] 8.3 Verify retrieval quality (relevant chunks returned)
- [ ] 8.4 Verify response quality (contextual, grounded in documents)
- [ ] 8.5 Test dark/light mode toggle functionality
- [ ] 8.6 Test all configuration parameters (top-k, threshold, temperature)
- [ ] 8.7 Test error scenarios (Ollama down, no documents, corrupted files)
- [ ] 8.8 Verify performance on CPU-only system (acceptable response times)
- [ ] 8.9 Test on different operating systems (Windows, Mac, Linux if possible)
- [ ] 8.10 Final review of code quality and documentation completeness
