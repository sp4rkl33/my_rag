## Why

The current RAG system only provides a Streamlit web UI, which requires a browser and runs a web server. Users who prefer working in the terminal or need a lightweight, fast interface for quick queries would benefit from a dedicated terminal application that provides an interactive command-line experience without the overhead of a web server.

## What Changes

- Add a terminal-based interactive application for RAG queries
- Implement a REPL (Read-Eval-Print Loop) with conversation history
- Support streaming responses in the terminal with rich formatting
- Provide slash commands for document management and configuration
- Include session persistence (save/load conversations)
- Add colorized output and progress indicators
- Create a Windows launcher script for easy access

## Capabilities

### New Capabilities
- `terminal-repl`: Interactive command-line REPL with conversation loop, history, and streaming responses
- `terminal-ui`: Rich terminal formatting with colors, progress indicators, and markdown rendering
- `session-management`: Save and load conversation sessions to/from JSON files
- `terminal-commands`: Slash commands for document operations, configuration, and session management

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

**New Files:**
- `terminal.py`: Main terminal application script
- `src/terminal_ui.py`: Terminal formatting and display utilities
- `src/session.py`: Conversation session management
- `sessions/`: Directory for storing conversation files
- `run_terminal.bat`: Windows launcher for terminal mode

**Modified Files:**
- `README.md`: Add documentation for terminal mode

**Dependencies:**
- Uses existing `rich` library (already in requirements.txt)
- No new dependencies required

**User Experience:**
- Users can run `python terminal.py` or `run_terminal.bat` for terminal-based interaction
- Existing web UI and CLI tools remain unchanged
- No breaking changes to current functionality
