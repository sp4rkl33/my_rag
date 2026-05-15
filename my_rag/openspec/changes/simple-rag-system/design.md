## Context

Building a local RAG system from scratch as an educational project to understand the internals of retrieval-augmented generation. The system will use entirely local models (no API dependencies) with a focus on learning how embeddings, vector databases, and LLMs integrate. The project requires a vibrant, modern UI to make the learning experience engaging and visually appealing.

Current state: Empty project directory. No existing RAG infrastructure.

Constraints:
- Must run entirely locally (no cloud APIs)
- Must support 8GB RAM minimum (target Llama 3.1 8B model)
- Must be educational and easy to understand (clear module separation)
- Must have vibrant, modern UI (not basic/boring interface)

## Goals / Non-Goals

**Goals:**
- Build complete RAG pipeline with clear phase separation for progressive learning
- Support PDF, TXT, and Markdown document ingestion
- Implement semantic search using local embeddings (sentence-transformers)
- Generate contextual responses using local Ollama LLM
- Create vibrant Streamlit UI with gradients, animations, dark/light modes
- Modular architecture where each component can be understood independently
- CLI tools for document ingestion and querying (in addition to web UI)

**Non-Goals:**
- Production-grade scalability (this is a learning project)
- Multi-user support or authentication
- Conversation history persistence across sessions
- Advanced chunking strategies (recursive, semantic)
- Hybrid search (keyword + vector)
- Reranking or query expansion
- Cloud deployment or API endpoints
- Support for other document types (DOCX, HTML, etc.)

## Decisions

### Decision 1: Use sentence-transformers for embeddings (not OpenAI)

**Choice:** `all-MiniLM-L6-v2` model from sentence-transformers

**Rationale:**
- Completely local, no API costs
- Small model size (80MB) loads quickly
- Good quality for general-purpose semantic search
- Well-documented and widely used in RAG tutorials

**Alternatives considered:**
- OpenAI embeddings: Rejected due to API costs and learning goal of local-first
- `all-mpnet-base-v2`: Better quality but 420MB, overkill for learning project
- `bge-small-en-v1.5`: Good alternative but less documentation

### Decision 2: Use ChromaDB for vector storage (not FAISS or Pinecone)

**Choice:** ChromaDB with persistent local storage

**Rationale:**
- Simple API, minimal setup
- Built-in persistence to disk (SQLite-based)
- Includes metadata filtering capabilities
- Good documentation and active community
- No server required (embedded mode)

**Alternatives considered:**
- FAISS: More performant but requires manual persistence and metadata management
- Pinecone: Cloud-based, conflicts with local-first goal
- Weaviate: Overkill, requires separate server process

### Decision 3: Use Ollama for LLM inference (not llama.cpp or transformers)

**Choice:** Ollama with Llama 3.1 8B model

**Rationale:**
- Zero-config installation and model management
- Automatic GPU detection and optimization
- OpenAI-compatible API (easy to use)
- Handles model quantization automatically
- Cross-platform (Windows/Mac/Linux)

**Alternatives considered:**
- llama.cpp: More control but requires manual setup and model conversion
- transformers library: Direct but requires more GPU memory management code
- GPT4All: Simpler but less powerful models

### Decision 4: Use Streamlit for web UI (not Flask/FastAPI + React)

**Choice:** Streamlit with custom CSS for vibrant theming

**Rationale:**
- Rapid development, minimal boilerplate
- Built-in widgets and layouts
- Easy to add custom CSS for gradients and animations
- Session state management included
- Perfect for data/ML applications

**Alternatives considered:**
- Flask + React: More flexible but 10x more code, overkill for learning project
- Gradio: Similar to Streamlit but less customizable for vibrant themes
- Pure HTML/CSS/JS: Too much frontend work, distracts from RAG learning

### Decision 5: Phased implementation approach

**Choice:** 4 distinct phases with clear boundaries

**Phase 1: Core RAG Pipeline**
- Embeddings generation
- Vector storage setup
- Basic retrieval

**Phase 2: LLM Integration**
- Ollama connection
- Prompt construction
- Response generation

**Phase 3: Document Ingestion**
- File parsing (PDF/TXT/MD)
- Chunking strategy
- Batch processing

**Phase 4: Vibrant Web UI**
- Streamlit interface
- Custom CSS theming
- Dark/light mode toggle
- Animations and gradients

**Rationale:**
- Each phase builds on previous (dependencies clear)
- Can test and validate each phase independently
- Progressive learning: understand one layer before adding next
- Can stop at any phase and still have working system

**Alternatives considered:**
- Build everything at once: Too overwhelming, hard to debug
- Different phase order: This order follows natural RAG flow (data → retrieval → generation → interface)

### Decision 6: Project structure - modular components

**Choice:** Separate Python modules for each capability

```
src/
├── embedder.py       # Embedding generation
├── vectorstore.py    # ChromaDB wrapper
├── retriever.py      # Search logic
├── llm.py           # Ollama interface
├── chunker.py       # Document chunking
├── parser.py        # File parsing
└── rag.py           # Main pipeline orchestration
```

**Rationale:**
- Clear separation of concerns
- Easy to understand each component in isolation
- Can test components independently
- Follows single responsibility principle

**Alternatives considered:**
- Single monolithic file: Easier to start but becomes unmaintainable
- Class-based architecture: More OOP but adds complexity for learning project

### Decision 7: Chunking strategy - fixed size with overlap

**Choice:** 500-1000 tokens per chunk, 100 token overlap

**Rationale:**
- Simple to implement and understand
- Overlap prevents context loss at boundaries
- Fits well within embedding model limits (512 tokens)
- Standard approach in RAG tutorials

**Alternatives considered:**
- Semantic chunking: More sophisticated but complex to implement
- Paragraph-based: Too variable in size, some paragraphs too large
- Sentence-based: Too granular, loses context

### Decision 8: UI theming - CSS-based gradients and animations

**Choice:** Custom CSS injected into Streamlit with:
- Linear gradients for backgrounds
- CSS transitions for smooth interactions
- CSS variables for dark/light mode switching
- Keyframe animations for loading states

**Rationale:**
- Full control over visual appearance
- No additional dependencies
- Performant (CSS animations are GPU-accelerated)
- Easy to customize and experiment

**Alternatives considered:**
- Streamlit themes only: Too limited, can't achieve vibrant gradients
- JavaScript animations: Overkill, adds complexity
- External CSS framework: Unnecessary dependency

## Risks / Trade-offs

### Risk: Ollama not installed or model not pulled
**Mitigation:** 
- Check Ollama connection on startup
- Provide clear error messages with installation instructions
- Include setup guide in README

### Risk: Insufficient RAM for Llama 3.1 8B
**Mitigation:**
- Document minimum 8GB RAM requirement
- Provide fallback instructions for Phi-3 Mini (2.3GB)
- Detect available memory and suggest appropriate model

### Risk: Slow inference on CPU-only systems
**Mitigation:**
- Set user expectations (20-60 sec response time on CPU)
- Show loading indicators in UI
- Document GPU benefits in README

### Risk: Poor retrieval quality with simple chunking
**Trade-off accepted:**
- This is a learning project, not production system
- Simple chunking is easier to understand
- Can be improved in future iterations

### Risk: ChromaDB storage grows large with many documents
**Mitigation:**
- Provide "clear database" function in UI
- Show storage size in UI
- Document expected storage requirements

### Risk: Custom CSS breaks with Streamlit updates
**Mitigation:**
- Pin Streamlit version in requirements.txt
- Use stable CSS selectors
- Test UI after any dependency updates

### Risk: PDF parsing fails on complex documents
**Mitigation:**
- Use pypdf library (handles most PDFs)
- Log parsing errors clearly
- Skip problematic files and continue processing

### Risk: Vibrant UI may be too colorful for some users
**Trade-off accepted:**
- Dark/light mode provides some customization
- This is an educational project, visual appeal is a feature
- Users can modify CSS if desired

## Migration Plan

Not applicable - this is a new project with no existing system to migrate from.

Deployment steps:
1. Install Python 3.10+
2. Install Ollama and pull llama3.1:8b model
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run ingestion: `python ingest.py --dir ./documents`
5. Launch UI: `streamlit run app.py`

## Open Questions

1. **Should we support conversation history?**
   - Leaning no: Adds complexity, not core to RAG learning
   - Could add in future iteration if desired

2. **Should we include example documents?**
   - Leaning yes: Include small sample dataset (Wikipedia articles, papers)
   - Helps users test immediately without finding documents

3. **Should CLI tools be interactive or script-based?**
   - Leaning script-based: Simpler, easier to understand
   - Can add interactive mode later if needed

4. **Should we include evaluation metrics (retrieval quality)?**
   - Leaning no: Out of scope for basic learning project
   - Could be interesting future addition

5. **Should we support multiple vector databases (FAISS, Pinecone)?**
   - Leaning no: Adds abstraction complexity
   - ChromaDB is sufficient for learning goals
