## 1. Session Class Updates

- [x] 1.1 Add get_context_window(n) method to return last n conversation turns
- [x] 1.2 Format conversation turns as simple dict with query/response
- [x] 1.3 Handle edge case when n is larger than history length
- [x] 1.4 Test get_context_window with various window sizes

## 2. LLM Prompt Construction

- [x] 2.1 Update construct_prompt() signature to accept optional conversation_history parameter
- [x] 2.2 Format conversation history as "User: ... Assistant: ..." pairs
- [x] 2.3 Prepend conversation history to the prompt before context and query
- [x] 2.4 Handle empty conversation history gracefully
- [x] 2.5 Test prompt construction with and without conversation history

## 3. RAGPipeline Integration

- [x] 3.1 Update query() method signature to accept optional conversation_history parameter
- [x] 3.2 Pass conversation_history to llm.construct_prompt()
- [x] 3.3 Ensure backward compatibility (parameter is optional)
- [x] 3.4 Test query with conversation history

## 4. Config Class Updates

- [x] 4.1 Add context_window parameter to Config class (default: 5)
- [x] 4.2 Add validation for context_window in validate_and_set() method
- [x] 4.3 Ensure context_window accepts 0 (to disable) and positive integers
- [x] 4.4 Add context_window to get_all() method
- [x] 4.5 Test context_window configuration

## 5. Terminal Main Loop Integration

- [x] 5.1 Get conversation context from session before querying
- [x] 5.2 Pass conversation history to pipeline.query()
- [x] 5.3 Use config.context_window to determine how many turns to include
- [x] 5.4 Handle context_window of 0 (skip passing conversation history)
- [x] 5.5 Test query flow with conversation memory enabled

## 6. Context Command Implementation

- [x] 6.1 Implement handle_context() command handler
- [x] 6.2 Display current conversation context window
- [x] 6.3 Show how many turns are being used for context
- [x] 6.4 Handle empty context gracefully
- [x] 6.5 Add "context" to COMMANDS registry

## 7. Config Command Updates

- [x] 7.1 Update handle_config() to display context_window parameter
- [x] 7.2 Update handle_set() to support context_window parameter
- [x] 7.3 Add validation error messages for invalid context_window values
- [x] 7.4 Test /config and /set commands with context_window

## 8. Help Command Updates

- [x] 8.1 Add /context command to help text
- [x] 8.2 Add context_window to configuration parameters documentation
- [x] 8.3 Update command-specific help for /context

## 9. Documentation

- [x] 9.1 Update README.md with conversation memory feature
- [x] 9.2 Document /context command
- [x] 9.3 Document context_window configuration parameter
- [x] 9.4 Add examples of follow-up questions
- [x] 9.5 Explain how to disable conversation memory

## 10. Testing

- [x] 10.1 Test basic follow-up question flow
- [x] 10.2 Test with different context_window sizes
- [x] 10.3 Test with context_window set to 0 (disabled)
- [x] 10.4 Test /context command
- [x] 10.5 Test conversation context after session save/load
- [x] 10.6 Test with long conversation exceeding context window
- [x] 10.7 Test /clear command clears context
- [x] 10.8 Verify backward compatibility with existing sessions
