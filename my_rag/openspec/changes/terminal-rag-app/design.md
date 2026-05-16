## Context

The RAG system currently provides a Streamlit web UI (app.py) and basic CLI tools (ingest.py, query.py). The CLI tools are single-shot commands without conversation state. Users need a terminal-based interactive mode that combines conversational experience with lightweight CLI performance.

Current state:
- `src/rag.py`: RAGPipeline class handles ingestion and querying
- `src/llm.py`: OllamaLLM supports streaming responses
- `src/vectorstore.py`: ChromaDB wrapper for document storage
- `requirements.txt`: Already includes `rich` library for terminal formatting

Constraints:
- Must work on Windows (user's environment)
- Must reuse existing RAG pipeline without duplication
- Must maintain compatibility with existing tools
- Should be lightweight (no heavy dependencies)

## Goals / Non-Goals

**Goals:**
- Create an interactive terminal REPL for conversational RAG queries
- Provide rich terminal formatting with colors and progress indicators
- Support session management (save/load conversations)
- Include slash commands for document and configuration management
- Stream LLM responses in real-time to the terminal
- Maintain conversation history within the session

**Non-Goals:**
- Multi-user support or authentication
- Full TUI framework (curses, textual)
- Real-time collaboration features
- Voice input/output
- Advanced terminal features (split panes, tabs)
- Integration with external chat platforms

## Decisions

### Decision 1: Use Python's built-in input() with Rich for formatting

**Choice:** Use standard `input()` for user input and `rich` library for output formatting

**Rationale:**
- `input()` is simple, cross-platform, and handles basic line editing
- `rich` provides colors, progress bars, and markdown rendering
- Already in requirements.txt, no new dependencies
- Works well on Windows without special configuration

**Alternatives considered:**
- `prompt_toolkit`: More features but adds complexity and dependency weight
- `curses`: Full TUI but not cross-platform (Windows issues) and overkill
- Plain print/input: Too basic, poor user experience

### Decision 2: Store sessions as JSON files in sessions/ directory

**Choice:** Save conversation history as JSON files with timestamp-based filenames

**Rationale:**
- Simple, human-readable format
- Easy to implement with Python's json module
- Users can inspect/edit sessions manually if needed
- No database dependency

**Alternatives considered:**
- SQLite database: Overkill for simple conversation storage
- Pickle files: Not human-readable, security concerns
- Plain text: Loses structure, harder to parse

### Decision 3: Implement command parser with simple string matching

**Choice:** Parse commands by checking if input starts with "/" and splitting on whitespace

**Rationale:**
- Simple to implement and understand
- Sufficient for the command set we need
- No regex complexity or parsing library needed
- Easy to extend with new commands

**Alternatives considered:**
- Regex-based parser: More flexible but harder to maintain
- argparse for each command: Too heavyweight
- Command framework (click, typer): Adds dependency and complexity

### Decision 4: Reuse existing RAGPipeline class without modification

**Choice:** Import and use `src/rag.py::RAGPipeline` directly

**Rationale:**
- No code duplication
- Ensures consistency across all interfaces
- Existing pipeline already supports streaming
- Changes to RAG logic automatically apply to terminal mode

**Alternatives considered:**
- Create separate terminal-specific pipeline: Code duplication
- Modify RAGPipeline for terminal mode: Breaks separation of concerns

### Decision 5: Use Rich Console for streaming output

**Choice:** Use `rich.console.Console` with live updates for streaming responses

**Rationale:**
- Rich handles terminal width, wrapping, and formatting automatically
- Supports markdown rendering for formatted responses
- Works well with streaming token generation
- Provides built-in progress indicators

**Alternatives considered:**
- Manual ANSI escape codes: Error-prone, hard to maintain
- Print with flush: No formatting, poor UX
- Separate library for streaming: Unnecessary additional dependency

### Decision 6: Store conversation history in memory, persist on demand

**Choice:** Keep conversation list in memory during session, save to file only when user requests or on exit

**Rationale:**
- Fast access during session
- No I/O overhead on every query
- User controls when to persist
- Simple implementation

**Alternatives considered:**
- Auto-save after every query: I/O overhead, unnecessary
- Database-backed history: Overkill for single-user local tool
- No persistence: Loses valuable conversation data

### Decision 7: Implement graceful error handling with continue-on-error

**Choice:** Catch exceptions, display error messages, and return to prompt rather than crashing

**Rationale:**
- Better user experience (don't lose session on error)
- Allows recovery from transient issues (Ollama restart)
- Matches REPL expectations (errors don't exit the loop)

**Alternatives considered:**
- Crash on error: Poor UX, loses session state
- Silent error handling: User doesn't know what went wrong
- Retry logic: Adds complexity, may hang on persistent errors

## Risks / Trade-offs

### Risk: Windows terminal encoding issues
**Mitigation:**
- Use UTF-8 encoding explicitly in file operations
- Rich library handles terminal encoding automatically
- Test on Windows environment (user's platform)

### Risk: Large conversation history consumes memory
**Trade-off accepted:**
- For typical usage (dozens of queries), memory impact is negligible
- User can /clear history if needed
- Could add max-history limit in future if needed

### Risk: Streaming may be slow on CPU-only systems
**Mitigation:**
- This is inherent to LLM inference, not specific to terminal mode
- Streaming provides feedback that generation is happening
- User can see partial responses while waiting

### Risk: Session files may accumulate over time
**Mitigation:**
- Use timestamped filenames so users can identify old sessions
- Document session file location in help
- User can manually delete old sessions

### Risk: Command parsing may conflict with queries starting with "/"
**Trade-off accepted:**
- Slash commands are standard in chat interfaces
- Unlikely users will query about "/" at start of sentence
- Can escape with "//" if needed (future enhancement)

### Risk: No input history (up arrow for previous commands)
**Trade-off accepted:**
- Built-in input() doesn't support readline history on Windows
- Adding prompt_toolkit would increase complexity
- Users can use /history command to view past queries
- Could add in future if highly requested

## Migration Plan

No migration needed - this is additive functionality.

Deployment steps:
1. Create `terminal.py` in project root
2. Create `src/terminal_ui.py` for formatting utilities
3. Create `src/session.py` for session management
4. Create `sessions/` directory for storing conversation files
5. Create `run_terminal.bat` Windows launcher
6. Update README.md with terminal mode documentation
7. Test on Windows environment

Rollback: Simply don't use terminal.py - existing interfaces remain unchanged.

## Open Questions

1. **Should we support multi-line input for complex queries?**
   - Leaning no: Adds complexity, most queries are single-line
   - Could add later if users request it

2. **Should we include command autocomplete?**
   - Leaning no: Would require prompt_toolkit dependency
   - Help command provides command discovery

3. **Should sessions be auto-loaded on startup?**
   - Leaning no: Start fresh by default, user can /load if needed
   - Could add --resume flag in future
