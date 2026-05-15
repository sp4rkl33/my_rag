## ADDED Requirements

### Requirement: Connect to local Ollama instance
The system SHALL communicate with a locally running Ollama server.

#### Scenario: Verify Ollama connection
- **WHEN** system initializes LLM component
- **THEN** system checks if Ollama is running and accessible at localhost:11434

#### Scenario: Handle Ollama not running
- **WHEN** Ollama is not running or not accessible
- **THEN** system provides clear error message with instructions to start Ollama

### Requirement: Use Llama 3.1 8B model
The system SHALL generate responses using the Llama 3.1 8B model via Ollama.

#### Scenario: Load model on first use
- **WHEN** system makes first LLM request
- **THEN** system ensures llama3.1:8b model is available in Ollama

#### Scenario: Model not installed
- **WHEN** llama3.1:8b model is not installed
- **THEN** system provides instructions to pull the model with `ollama pull llama3.1:8b`

### Requirement: Construct context-aware prompts
The system SHALL build prompts that combine retrieved context with user queries.

#### Scenario: Build RAG prompt
- **WHEN** system has retrieved relevant chunks and user query
- **THEN** system constructs prompt with format: system instruction + retrieved context + user question

#### Scenario: Handle no retrieved context
- **WHEN** vector search returns no relevant chunks
- **THEN** system informs LLM that no relevant context was found and asks it to respond accordingly

#### Scenario: Limit context length
- **WHEN** retrieved chunks exceed token limit
- **THEN** system truncates context to fit within model's context window (8192 tokens)

### Requirement: Generate contextual responses
The system SHALL produce answers grounded in retrieved document content.

#### Scenario: Generate answer with citations
- **WHEN** LLM generates a response
- **THEN** response is based on provided context and includes source references

#### Scenario: Stream response tokens
- **WHEN** LLM generates a response
- **THEN** system streams tokens as they are generated for real-time display

#### Scenario: Handle generation errors
- **WHEN** LLM encounters an error during generation
- **THEN** system catches error and returns user-friendly error message

### Requirement: Configure generation parameters
The system SHALL allow customization of LLM behavior.

#### Scenario: Set temperature
- **WHEN** user configures temperature parameter
- **THEN** system uses specified temperature (0.0-1.0) for response generation

#### Scenario: Set max tokens
- **WHEN** user configures max output tokens
- **THEN** system limits response length to specified token count

#### Scenario: Use default parameters
- **WHEN** no parameters are specified
- **THEN** system uses defaults: temperature=0.7, max_tokens=512

### Requirement: Provide response metadata
The system SHALL return generation metadata alongside responses.

#### Scenario: Include generation stats
- **WHEN** system completes response generation
- **THEN** system returns response text, token count, generation time, and model used

#### Scenario: Track context usage
- **WHEN** system generates response
- **THEN** system reports number of context chunks used and their sources
