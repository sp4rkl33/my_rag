## ADDED Requirements

### Requirement: Save conversation session
The system SHALL allow users to save conversation sessions to JSON files.

#### Scenario: Save with filename
- **WHEN** user types "/save <filename>" command
- **THEN** system saves the session to the specified file in the sessions/ directory

#### Scenario: Save without filename
- **WHEN** user types "/save" command
- **THEN** system generates a timestamped filename and saves the session

#### Scenario: Overwrite confirmation
- **WHEN** user saves to an existing filename
- **THEN** system prompts for confirmation before overwriting

#### Scenario: Save success message
- **WHEN** session is saved successfully
- **THEN** system displays a success message with the file path

### Requirement: Load conversation session
The system SHALL allow users to load previous conversation sessions.

#### Scenario: Load session
- **WHEN** user types "/load <filename>" command
- **THEN** system loads the conversation history from the file

#### Scenario: File not found
- **WHEN** user tries to load a non-existent file
- **THEN** system displays an error message with available session files

#### Scenario: Load with current history
- **WHEN** user loads a session while having unsaved history
- **THEN** system prompts to save current session before loading

#### Scenario: Load success message
- **WHEN** session is loaded successfully
- **THEN** system displays a success message and shows the loaded conversation count

### Requirement: List saved sessions
The system SHALL allow users to view available saved sessions.

#### Scenario: List sessions
- **WHEN** user types "/sessions" command
- **THEN** system displays all saved session files with timestamps and conversation counts

#### Scenario: No saved sessions
- **WHEN** user types "/sessions" and no sessions exist
- **THEN** system displays a message indicating no saved sessions are available

### Requirement: Auto-save prompt on exit
The system SHALL prompt to save unsaved conversations on exit.

#### Scenario: Exit with unsaved history
- **WHEN** user exits with unsaved conversation history
- **THEN** system prompts to save the session before exiting

#### Scenario: Exit with no history
- **WHEN** user exits with no conversation history
- **THEN** system exits immediately without prompting

#### Scenario: Exit with saved session
- **WHEN** user exits and session is already saved
- **THEN** system exits immediately without prompting

### Requirement: Session file format
The system SHALL store sessions in a structured JSON format.

#### Scenario: Session structure
- **WHEN** session is saved
- **THEN** file contains timestamp, model name, and array of query/response pairs

#### Scenario: Session metadata
- **WHEN** session is saved
- **THEN** file includes metadata such as creation date and conversation count
