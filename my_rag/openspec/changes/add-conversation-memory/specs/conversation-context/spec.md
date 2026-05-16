## ADDED Requirements

### Requirement: Conversation history tracking
The system SHALL maintain a history of conversation turns (user queries and assistant responses) within the current session.

#### Scenario: First query in session
- **WHEN** user asks their first question in a new session
- **THEN** system stores the query and response as the first conversation turn

#### Scenario: Subsequent queries
- **WHEN** user asks follow-up questions
- **THEN** system appends each query/response pair to the conversation history

#### Scenario: Session cleared
- **WHEN** user executes /clear command
- **THEN** system removes all conversation history

### Requirement: Context window management
The system SHALL include a configurable number of recent conversation turns when constructing prompts for the LLM.

#### Scenario: Default context window
- **WHEN** conversation memory is enabled with default settings
- **THEN** system includes the last 5 conversation turns in the LLM prompt

#### Scenario: Custom context window
- **WHEN** user sets context_window to a specific value
- **THEN** system includes that many recent conversation turns in the LLM prompt

#### Scenario: Context window of zero
- **WHEN** user sets context_window to 0
- **THEN** system disables conversation memory and treats each query independently

### Requirement: Conversation context in prompts
The system SHALL include conversation history in the LLM prompt to enable contextual responses.

#### Scenario: Follow-up question
- **WHEN** user asks a follow-up question that references previous conversation
- **THEN** system includes recent conversation turns in the prompt so the LLM can understand the context

#### Scenario: First query
- **WHEN** user asks their first question with no prior conversation
- **THEN** system constructs prompt without conversation history

#### Scenario: Long conversation
- **WHEN** conversation exceeds the context window size
- **THEN** system includes only the most recent N turns as configured

### Requirement: Context command
The system SHALL provide a /context command to view the current conversation context.

#### Scenario: View current context
- **WHEN** user types /context command
- **THEN** system displays the conversation turns currently being used for context

#### Scenario: Empty context
- **WHEN** user types /context with no conversation history
- **THEN** system displays a message indicating no context is available

### Requirement: Context window configuration
The system SHALL allow users to configure the conversation context window size.

#### Scenario: Set context window
- **WHEN** user types /set context_window <n>
- **THEN** system updates the context window to include n recent conversation turns

#### Scenario: Invalid context window
- **WHEN** user tries to set context_window to a negative number
- **THEN** system displays an error message with valid range

#### Scenario: View context window setting
- **WHEN** user types /config context_window
- **THEN** system displays the current context window size

### Requirement: Conversation memory toggle
The system SHALL allow users to enable or disable conversation memory.

#### Scenario: Disable conversation memory
- **WHEN** user sets context_window to 0
- **THEN** system treats each query independently without conversation context

#### Scenario: Re-enable conversation memory
- **WHEN** user sets context_window to a positive number after disabling
- **THEN** system resumes including conversation history in prompts

### Requirement: Context preservation across commands
The system SHALL maintain conversation context when users execute slash commands.

#### Scenario: Command execution
- **WHEN** user executes a slash command like /list or /config
- **THEN** system preserves conversation history and continues using it for subsequent queries

#### Scenario: Session save and load
- **WHEN** user saves and loads a session
- **THEN** system restores conversation history and resumes using it for context
