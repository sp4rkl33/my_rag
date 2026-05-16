# Simple RAG System

A local Retrieval-Augmented Generation (RAG) system built for learning purposes. Uses entirely local models with no API dependencies.

## Features

- **Local-First**: sentence-transformers embeddings, ChromaDB vector store, Ollama LLM
- **Document Support**: PDF, TXT, and Markdown files
- **Semantic Search**: Vector-based similarity search with configurable parameters
- **Vibrant UI**: Modern Streamlit interface with gradients, animations, and dark/light modes
- **CLI Tools**: Command-line scripts for ingestion and querying

## System Requirements

### Minimum
- **RAM**: 8GB (for Llama 3.1 8B model)
- **Disk Space**: 10GB (5GB for model, rest for dependencies and data)
- **Python**: 3.10 or higher
- **OS**: Windows, macOS, or Linux

### Recommended
- **RAM**: 16GB
- **GPU**: NVIDIA GPU with 6GB+ VRAM (10x faster inference)
- **Disk Space**: 20GB

## Installation

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

**macOS/Linux:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**
Download and install from [ollama.com](https://ollama.com/download)

### 3. Pull Llama 3.1 8B Model

```bash
ollama pull llama3.1:8b
```

This will download ~5GB. For systems with less RAM, use a smaller model:
```bash
ollama pull phi3:mini
```

### 4. Verify Installation

Start Ollama (if not already running):
```bash
ollama serve
```

Test the model:
```bash
ollama run llama3.1:8b "Hello!"
```

## Usage

### Terminal Mode (Interactive)

Launch the interactive terminal interface for conversational RAG queries:

**Windows:**
```bash
run_terminal.bat
```

**macOS/Linux:**
```bash
python terminal.py
```

This starts an interactive REPL where you can have ongoing conversations with your documents. Simply type your questions and get streaming responses.

Features:
- Interactive REPL with conversation history
- **Conversation Memory**: AI remembers previous questions and answers for natural follow-up questions
- Streaming responses in real-time
- Rich terminal formatting with colors
- Session management (save/load conversations)
- Slash commands for document and configuration management

**Available Commands:**
- `/help` - Show available commands
- `/history [n]` - View conversation history
- `/context` - View current conversation context being used for memory
- `/clear` - Clear conversation history
- `/save [filename]` - Save current session
- `/load <filename>` - Load a previous session
- `/sessions` - List all saved sessions
- `/list` - Show ingested documents
- `/upload <filepath>` - Upload and ingest documents
- `/config [parameter]` - View configuration
- `/set <parameter> <value>` - Change configuration
- `/exit` or `/quit` - Exit the application

**Configuration Parameters:**
- `model` - LLM model name (default: llama3.1:8b)
- `top_k` - Number of documents to retrieve (1-20, default: 5)
- `temperature` - LLM temperature (0-2, default: 0.7)
- `threshold` - Similarity threshold (0-1, default: 0.3)
- `context_window` - Number of conversation turns to remember (0 to disable, default: 5)

**Example Session:**
```
llama3.1:8b> What is RAG?
[Streaming response about RAG...]

llama3.1:8b> Can you give me an example?
[AI remembers the previous question about RAG and provides a relevant example]

llama3.1:8b> What are the main components?
[AI continues the conversation about RAG components]

llama3.1:8b> /context
Conversation Context (last 3 turns):
1. User: What is RAG?
   Assistant: [response summary...]
2. User: Can you give me an example?
   Assistant: [response summary...]
3. User: What are the main components?
   Assistant: [response summary...]

llama3.1:8b> /save my-session
✓ Session saved to: sessions/my-session.json

llama3.1:8b> /exit
```

**Conversation Memory:**

The terminal mode includes conversation memory that allows the AI to remember previous questions and answers within a session. This enables natural follow-up questions without repeating context.

- **Default behavior**: Remembers last 5 conversation turns
- **View context**: Use `/context` to see what the AI remembers
- **Adjust memory**: Use `/set context_window <n>` to change how many turns to remember
- **Disable memory**: Use `/set context_window 0` to disable conversation memory
- **Clear memory**: Use `/clear` to reset the conversation history

Examples of follow-up questions:
- "What is machine learning?" → "Can you explain that in simpler terms?"
- "How does RAG work?" → "What are its advantages?" → "Are there any limitations?"
- "Tell me about the document" → "What does it say about X?" → "Can you elaborate on that?"

### Web UI

Launch the Streamlit interface:
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

Features:
- Upload documents via drag-and-drop
- Ask questions in chat interface
- View source citations
- Configure retrieval and generation parameters
- Toggle dark/light mode

### CLI Tools

**Ingest documents:**
```bash
# Ingest a single file
python ingest.py --file path/to/document.pdf

# Ingest a directory
python ingest.py --dir path/to/documents/
```

**Query from command line:**
```bash
python query.py "What is the main topic of the documents?"
```

## Project Structure

```
my_rag/
├── src/
│   ├── embedder.py       # Embedding generation (sentence-transformers)
│   ├── vectorstore.py    # ChromaDB wrapper
│   ├── retriever.py      # Similarity search
│   ├── llm.py           # Ollama LLM interface
│   ├── chunker.py       # Document chunking
│   ├── parser.py        # File parsing (PDF/TXT/MD)
│   └── rag.py           # Main pipeline orchestrator
├── data/
│   └── documents/       # Place your documents here
├── storage/
│   └── chroma/          # Vector database storage
├── app.py               # Streamlit web UI
├── ingest.py            # CLI ingestion tool
├── query.py             # CLI query tool
└── requirements.txt     # Python dependencies
```

## How It Works

1. **Document Ingestion**
   - Parse documents (PDF/TXT/MD)
   - Split into chunks (500-1000 tokens, 100 token overlap)
   - Generate embeddings using `all-MiniLM-L6-v2`
   - Store in ChromaDB with metadata

2. **Query Processing**
   - Embed user query with same model
   - Search ChromaDB for top-k similar chunks
   - Filter by similarity threshold (default: 0.3)

3. **Response Generation**
   - Construct prompt with retrieved context
   - Send to Ollama (Llama 3.1 8B)
   - Stream response tokens in real-time

## Configuration

Default parameters (configurable in UI or code):
- **Top-K Results**: 5
- **Similarity Threshold**: 0.3
- **Temperature**: 0.7
- **Max Tokens**: 512
- **Chunk Size**: 500-1000 tokens
- **Chunk Overlap**: 100 tokens

## Troubleshooting

### Ollama Connection Error
```
Error: Could not connect to Ollama at localhost:11434
```
**Solution**: Start Ollama with `ollama serve`

### Model Not Found
```
Error: Model llama3.1:8b not found
```
**Solution**: Pull the model with `ollama pull llama3.1:8b`

### Out of Memory
```
Error: Insufficient memory to load model
```
**Solution**: Use a smaller model like `phi3:mini` (2.3GB)

### Slow Inference (CPU)
Response times on CPU-only systems: 20-60 seconds per query.
**Solution**: Use a GPU for 10x faster inference, or use a smaller model.

### PDF Parsing Errors
Some complex PDFs may fail to parse.
**Solution**: The system will skip problematic files and continue. Check logs for details.

## Performance Notes

- **With GPU**: 2-5 seconds per response
- **CPU Only**: 20-60 seconds per response
- **Retrieval**: <1 second for databases with 1000+ chunks
- **Storage**: ~1MB per 100 document chunks

## Learning Resources

This is an educational project. Key concepts demonstrated:
- Vector embeddings and semantic search
- RAG architecture and prompt engineering
- Local LLM inference with Ollama
- Document chunking strategies
- Streamlit UI development

## License

MIT License - Free to use and modify for learning purposes.
