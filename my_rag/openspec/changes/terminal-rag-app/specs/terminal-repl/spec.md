## ADDED Requirements

### Requirement: Interactive conversation loop
The system SHALL provide a REPL that accepts user queries and returns RAG-generated responses in real-time.

#### Scenario: User enters a query
- **WHEN** user types a question and presses Enter
- **THEN** system retrieves relevant documents, generates a response, and displays it in the terminal

#### Scenario: Empty input handling
- **WHEN** user presses Enter without typing anything
- **THEN** system displays the prompt again without processing

#### Scenario: Exit the application
- **WHEN** user types "exit", "quit", or presses Ctrl+D
- **THEN** system prompts to save session if unsaved, then exits gracefully

### Requirement: Streaming response display
The system SHALL stream LLM responses token-by-token to the terminal as they are generated.

#### Scenario: Response streaming
- **WHEN** LLM generates a response
- **THEN** tokens appear in the terminal progressively without waiting for completion

#### Scenario: Interrupt streaming
- **WHEN** user presses Ctrl+C during response generation
- **THEN** system stops streaming and returns to the prompt

### Requirement: Conversation history
The system SHALL maintain conversation history within the current session.

#### Scenario: View conversation history
- **WHEN** user types "/history" command
- **THEN** system displays all previous queries and responses from the current session

#### Scenario: Clear conversation history
- **WHEN** user types "/clear" command
- **THEN** system clears the conversation history and confirms the action

#### Scenario: Limited history view
- **WHEN** user types "/history <n>" command
- **THEN** system displays the last n conversation turns

### Requirement: Error handling
The system SHALL handle errors gracefully without crashing the REPL.

#### Scenario: Ollama connection error
- **WHEN** Ollama service is not running
- **THEN** system displays a clear error message with instructions to start Ollama

#### Scenario: Document parsing error
- **WHEN** document upload fails due to parsing issues
- **THEN** system displays the error and continues accepting commands

#### Scenario: Invalid command
- **WHEN** user enters an unrecognized command
- **THEN** system displays "Unknown command" message and suggests "/help"

### Requirement: Startup checks
The system SHALL verify required services are available on startup.

#### Scenario: Ollama availability check
- **WHEN** terminal app starts
- **THEN** system checks if Ollama is running and displays a warning if not

#### Scenario: Empty document store warning
- **WHEN** terminal app starts with no documents ingested
- **THEN** system displays a message suggesting to upload documents
