## ADDED Requirements

### Requirement: Command prefix
The system SHALL recognize commands that start with a forward slash (/) to distinguish them from regular queries.

#### Scenario: Command execution
- **WHEN** user input starts with "/"
- **THEN** system interprets it as a command rather than a query

#### Scenario: Regular query
- **WHEN** user input does not start with "/"
- **THEN** system processes it as a RAG query

### Requirement: Help command
The system SHALL provide a /help command that displays available commands.

#### Scenario: List all commands
- **WHEN** user types "/help"
- **THEN** system displays all available commands with brief descriptions

#### Scenario: Command-specific help
- **WHEN** user types "/help <command>"
- **THEN** system displays detailed usage and examples for that command

### Requirement: History command
The system SHALL provide a /history command to view conversation history.

#### Scenario: Show full history
- **WHEN** user types "/history"
- **THEN** system displays all queries and responses from the current session

#### Scenario: Show limited history
- **WHEN** user types "/history <n>"
- **THEN** system displays the last n conversation turns

### Requirement: Clear command
The system SHALL provide a /clear command to reset conversation history.

#### Scenario: Clear history
- **WHEN** user types "/clear"
- **THEN** system clears conversation history and displays confirmation

#### Scenario: Clear with unsaved warning
- **WHEN** user types "/clear" and there is unsaved history
- **THEN** system prompts for confirmation before clearing

### Requirement: Save command
The system SHALL provide a /save command to persist conversation sessions.

#### Scenario: Save with filename
- **WHEN** user types "/save <filename>"
- **THEN** system saves the session to the specified file

#### Scenario: Save without filename
- **WHEN** user types "/save"
- **THEN** system generates a timestamped filename and saves the session

### Requirement: Load command
The system SHALL provide a /load command to restore previous sessions.

#### Scenario: Load session
- **WHEN** user types "/load <filename>"
- **THEN** system loads the conversation history from the file

#### Scenario: File not found
- **WHEN** user tries to load a non-existent file
- **THEN** system displays an error message with available session files

### Requirement: Sessions command
The system SHALL provide a /sessions command to list saved sessions.

#### Scenario: List sessions
- **WHEN** user types "/sessions"
- **THEN** system displays all saved session files with metadata

### Requirement: List command
The system SHALL provide a /list command to display ingested documents.

#### Scenario: List all documents
- **WHEN** user types "/list"
- **THEN** system displays document names, IDs, and ingestion dates in a table

#### Scenario: Empty document store
- **WHEN** user types "/list" and no documents are ingested
- **THEN** system displays a message indicating no documents are available

### Requirement: Upload command
The system SHALL provide an /upload command to ingest documents.

#### Scenario: Upload single file
- **WHEN** user types "/upload <filepath>"
- **THEN** system ingests the document and displays progress and confirmation

#### Scenario: Upload multiple files
- **WHEN** user types "/upload <filepath1> <filepath2> ..."
- **THEN** system ingests all documents sequentially with progress for each

#### Scenario: Invalid file path
- **WHEN** user provides a non-existent file path
- **THEN** system displays an error message and continues accepting commands

### Requirement: Config command
The system SHALL provide a /config command to view current settings.

#### Scenario: View all settings
- **WHEN** user types "/config"
- **THEN** system displays current configuration (model, top-k, temperature, threshold)

#### Scenario: View specific setting
- **WHEN** user types "/config <parameter>"
- **THEN** system displays the current value of that parameter

### Requirement: Set command
The system SHALL provide a /set command to change configuration parameters.

#### Scenario: Set parameter
- **WHEN** user types "/set <parameter> <value>"
- **THEN** system updates the parameter and displays confirmation

#### Scenario: Invalid parameter
- **WHEN** user tries to set an invalid parameter
- **THEN** system displays an error with valid parameter names

#### Scenario: Invalid value
- **WHEN** user provides an invalid value for a parameter
- **THEN** system displays an error with valid value range or options

### Requirement: Exit command
The system SHALL provide exit commands to terminate the session.

#### Scenario: Exit command
- **WHEN** user types "/exit" or "/quit"
- **THEN** system prompts to save if there is unsaved history, then exits

#### Scenario: Force exit
- **WHEN** user presses Ctrl+C or Ctrl+D
- **THEN** system exits with a goodbye message after save prompt if needed
