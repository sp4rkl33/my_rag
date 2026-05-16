## 1. Project Structure Setup

- [x] 1.1 Create sessions/ directory for storing conversation files
- [x] 1.2 Create src/terminal_ui.py module for terminal formatting utilities
- [x] 1.3 Create src/session.py module for session management
- [x] 1.4 Create terminal.py main script in project root

## 2. Session Management (src/session.py)

- [x] 2.1 Implement Session class to store conversation history
- [x] 2.2 Add method to append query/response pairs to history
- [x] 2.3 Implement save_to_file() method to persist session as JSON
- [x] 2.4 Implement load_from_file() method to restore session from JSON
- [x] 2.5 Add method to clear conversation history
- [x] 2.6 Add method to get formatted history for display
- [x] 2.7 Add timestamp generation for auto-named session files
- [x] 2.8 Add method to list available session files

## 3. Terminal UI Utilities (src/terminal_ui.py)

- [x] 3.1 Create TerminalUI class with Rich Console instance
- [x] 3.2 Implement display_welcome() to show startup banner
- [x] 3.3 Implement display_prompt() to show input prompt with model name
- [x] 3.4 Implement display_query() to show user input in cyan color
- [x] 3.5 Implement display_response() to show assistant response with formatting
- [x] 3.6 Implement display_sources() to show retrieved document citations
- [x] 3.7 Implement display_error() to show error messages in red
- [x] 3.8 Implement display_success() to show success messages in green
- [x] 3.9 Implement display_info() to show informational messages in gray
- [x] 3.10 Implement show_spinner() context manager for progress indicators
- [x] 3.11 Implement stream_response() to display streaming tokens in real-time
- [x] 3.12 Implement display_table() for formatted document lists

## 4. Command Parser (terminal.py)

- [x] 4.1 Implement is_command() function to check if input starts with "/"
- [x] 4.2 Implement parse_command() to extract command name and arguments
- [x] 4.3 Create command registry dictionary mapping command names to handlers
- [x] 4.4 Implement handle_help() for /help command
- [x] 4.5 Implement handle_history() for /history command
- [x] 4.6 Implement handle_clear() for /clear command
- [x] 4.7 Implement handle_save() for /save command
- [x] 4.8 Implement handle_load() for /load command
- [x] 4.9 Implement handle_sessions() for /sessions command
- [x] 4.10 Implement handle_list() for /list command
- [x] 4.11 Implement handle_upload() for /upload command
- [x] 4.12 Implement handle_config() for /config command
- [x] 4.13 Implement handle_set() for /set command
- [x] 4.14 Implement handle_exit() for /exit and /quit commands

## 5. Main REPL Loop (terminal.py)

- [x] 5.1 Initialize RAGPipeline instance
- [x] 5.2 Initialize Session instance for conversation history
- [x] 5.3 Initialize TerminalUI instance
- [x] 5.4 Display welcome banner with instructions
- [x] 5.5 Check Ollama availability on startup
- [x] 5.6 Check document store status on startup
- [x] 5.7 Implement main loop to read user input
- [x] 5.8 Add command detection and routing logic
- [x] 5.9 Implement query processing for non-command input
- [x] 5.10 Add streaming response display with token-by-token output
- [x] 5.11 Store query/response pairs in session history
- [x] 5.12 Handle empty input (skip processing, show prompt again)
- [x] 5.13 Handle Ctrl+C during response streaming (stop and return to prompt)
- [x] 5.14 Handle Ctrl+D and Ctrl+C for exit (prompt to save if unsaved)
- [x] 5.15 Add exception handling with error display and continue-on-error

## 6. Command Implementations

- [x] 6.1 /help: Display all commands with descriptions
- [x] 6.2 /help <command>: Display detailed help for specific command
- [x] 6.3 /history: Display all conversation turns with formatting
- [x] 6.4 /history <n>: Display last n conversation turns
- [x] 6.5 /clear: Clear conversation history with confirmation if unsaved
- [x] 6.6 /save: Generate timestamped filename and save session
- [x] 6.7 /save <filename>: Save session to specified file
- [x] 6.8 /save with overwrite confirmation for existing files
- [x] 6.9 /load <filename>: Load session from file
- [x] 6.10 /load with save prompt if current session is unsaved
- [x] 6.11 /load error handling for non-existent files
- [x] 6.12 /sessions: Display all saved sessions with metadata
- [x] 6.13 /list: Display all documents in table format with IDs and dates
- [x] 6.14 /upload <filepath>: Ingest document with progress indicator
- [x] 6.15 /upload with multiple file support
- [x] 6.16 /upload error handling for invalid paths
- [x] 6.17 /config: Display all current settings in table format
- [x] 6.18 /config <parameter>: Display specific parameter value
- [x] 6.19 /set <parameter> <value>: Update parameter with validation
- [x] 6.20 /set error handling for invalid parameters and values
- [x] 6.21 /exit and /quit: Prompt to save if unsaved, then exit gracefully

## 7. Configuration Management

- [x] 7.1 Create Config class to store RAG parameters
- [x] 7.2 Add default values (model, top_k, temperature, threshold)
- [x] 7.3 Implement parameter validation for /set command
- [x] 7.4 Apply config changes to RAGPipeline dynamically
- [x] 7.5 Add method to get formatted config for display

## 8. Error Handling

- [x] 8.1 Handle Ollama connection errors with helpful message
- [x] 8.2 Handle document parsing errors without crashing
- [x] 8.3 Handle file I/O errors for session save/load
- [x] 8.4 Handle invalid command errors with suggestion to use /help
- [x] 8.5 Handle keyboard interrupts (Ctrl+C) gracefully
- [x] 8.6 Handle EOF (Ctrl+D) for exit
- [x] 8.7 Add try-catch around main loop to prevent crashes

## 9. Windows Launcher Script

- [x] 9.1 Create run_terminal.bat for Windows
- [x] 9.2 Add virtual environment activation
- [x] 9.3 Add Ollama connection check
- [x] 9.4 Launch terminal.py with proper error handling
- [x] 9.5 Add deactivate on exit

## 10. Documentation

- [x] 10.1 Add "Terminal Mode" section to README.md
- [x] 10.2 Document how to launch terminal mode
- [x] 10.3 Document available slash commands
- [x] 10.4 Document session management (save/load)
- [x] 10.5 Add examples of common workflows
- [x] 10.6 Document configuration parameters

## 11. Testing

- [x] 11.1 Test basic query/response flow
- [x] 11.2 Test all slash commands individually
- [x] 11.3 Test session save and load
- [x] 11.4 Test document upload
- [x] 11.5 Test configuration changes
- [x] 11.6 Test error handling (Ollama down, invalid files, etc.)
- [x] 11.7 Test Ctrl+C and Ctrl+D handling
- [x] 11.8 Test on Windows environment
- [x] 11.9 Test with empty document store
- [x] 11.10 Test with long conversation history
