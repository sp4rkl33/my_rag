## ADDED Requirements

### Requirement: Colored output
The system SHALL use colors to distinguish different types of content in the terminal.

#### Scenario: User query display
- **WHEN** user enters a query
- **THEN** system displays it in cyan color to differentiate from responses

#### Scenario: System response display
- **WHEN** system generates a response
- **THEN** response text is displayed with proper formatting and default color

#### Scenario: Error message display
- **WHEN** an error occurs
- **THEN** error messages are displayed in red with an error icon

#### Scenario: Success message display
- **WHEN** a command completes successfully
- **THEN** success messages are displayed in green with a checkmark icon

#### Scenario: Command output display
- **WHEN** user executes a slash command
- **THEN** command output is displayed in a muted color to distinguish from conversation

### Requirement: Progress indicators
The system SHALL display progress indicators for long-running operations.

#### Scenario: Document ingestion progress
- **WHEN** user uploads a document
- **THEN** system displays a spinner during parsing and embedding

#### Scenario: Retrieval indicator
- **WHEN** system searches the vector database
- **THEN** system displays a "Searching..." indicator

#### Scenario: Response generation indicator
- **WHEN** waiting for LLM to start streaming
- **THEN** system displays a "Thinking..." indicator until first token arrives

### Requirement: Formatted text rendering
The system SHALL render markdown-like formatting in terminal output.

#### Scenario: Bold text
- **WHEN** response contains bold markers
- **THEN** system renders text in bold using terminal formatting

#### Scenario: Code blocks
- **WHEN** response contains code blocks
- **THEN** system displays them with syntax highlighting and proper indentation

#### Scenario: Lists
- **WHEN** response contains bullet or numbered lists
- **THEN** system formats them with proper indentation and markers

### Requirement: Source citation display
The system SHALL display retrieved document sources in a readable format.

#### Scenario: Show sources
- **WHEN** response is generated from retrieved documents
- **THEN** system displays source citations with document names and relevance scores

### Requirement: Terminal width adaptation
The system SHALL adapt output formatting to the current terminal width.

#### Scenario: Text wrapping
- **WHEN** response text exceeds terminal width
- **THEN** system wraps text at word boundaries without breaking formatting

#### Scenario: Table formatting
- **WHEN** displaying tabular data
- **THEN** system adjusts column widths to fit terminal width

### Requirement: Welcome banner
The system SHALL display a welcome banner on startup.

#### Scenario: Startup banner
- **WHEN** terminal app starts
- **THEN** system displays a welcome message with app name, version, and basic instructions

### Requirement: Input prompt
The system SHALL display a clear and informative prompt.

#### Scenario: Default prompt
- **WHEN** waiting for user input
- **THEN** system displays a prompt showing the current model name

#### Scenario: Prompt after response
- **WHEN** response completes
- **THEN** system displays the prompt on a new line ready for next input
