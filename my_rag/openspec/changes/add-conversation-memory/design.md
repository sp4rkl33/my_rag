## Context

The terminal RAG app currently treats each query independently. The `Session` class stores conversation history for persistence (save/load), but this history is not used when constructing prompts for the LLM. Each query only includes the current question and retrieved document context, without any previous conversation turns.

Current state:
- `src/session.py`: Stores conversation history as list of query/response pairs
- `src/llm.py`: `construct_prompt()` only accepts query and context chunks
- `terminal.py`: Calls `pipeline.query()` with only the current query
- No conversation context is passed to the LLM

Constraints:
- Must maintain backward compatibility with existing session files
- Must not exceed LLM context window limits
- Should be configurable (users may want to disable it)
- Must work with streaming responses

## Goals / Non-Goals

**Goals:**
- Enable the LLM to remember and reference previous conversation turns
- Allow users to ask follow-up questions naturally
- Provide configurable context window size
- Add commands to view and control conversation context
- Maintain conversation context across session save/load

**Non-Goals:**
- Long-term memory across sessions (only current session)
- Semantic search over conversation history
- Conversation summarization or compression
- Multi-user conversation tracking
- Conversation branching or forking

## Decisions

### Decision 1: Include conversation history in LLM prompt

**Choice:** Modify `construct_prompt()` to accept optional conversation history and prepend it to the prompt

**Rationale:**
- Simple to implement - just format and prepend to existing prompt
- Works with existing streaming infrastructure
- LLM naturally handles conversation context in prompts
- No changes to Ollama API calls needed

**Alternatives considered:**
- Use Ollama's chat API: More complex, would require rewriting LLM interface
- Store conversation in vector database: Overkill, adds complexity
- Use separate conversation model: Unnecessary, single model can handle it

### Decision 2: Store context window size in Config class

**Choice:** Add `context_window` parameter to Config (default: 5)

**Rationale:**
- Consistent with other configuration parameters
- Easy to modify with `/set` command
- Persists across queries in same session
- Setting to 0 disables conversation memory

**Alternatives considered:**
- Global constant: Not user-configurable
- Per-query parameter: Too granular, confusing UX
- Automatic based on token count: Complex, unpredictable behavior

### Decision 3: Format conversation history as "User: ... Assistant: ..." pairs

**Choice:** Format conversation turns as simple labeled exchanges in the prompt

**Rationale:**
- Clear and readable format
- Standard pattern used by many chat models
- Easy to parse visually when debugging
- Works well with instruction-following models

**Alternatives considered:**
- JSON format: Less natural for LLM to process
- XML tags: More verbose, no benefit
- Just concatenate: Ambiguous who said what

### Decision 4: Limit context window by number of turns, not tokens

**Choice:** Use fixed number of recent conversation turns (e.g., last 5)

**Rationale:**
- Simple to implement and understand
- Predictable behavior for users
- Avoids complex token counting logic
- Good enough for most conversations

**Alternatives considered:**
- Token-based limit: More accurate but complex to implement
- Time-based limit: Doesn't correlate with context relevance
- Automatic based on relevance: Too complex, unpredictable

### Decision 5: Add conversation history to Session.get_formatted_history()

**Choice:** Create new method `get_context_window(n)` in Session class

**Rationale:**
- Separates concerns (display vs context)
- Returns only what's needed for LLM prompt
- Doesn't modify existing `get_formatted_history()` behavior
- Easy to test independently

**Alternatives considered:**
- Modify existing method: Could break existing code
- Add parameter to existing method: Less clear intent
- Do formatting in terminal.py: Violates separation of concerns

### Decision 6: Pass conversation history through RAGPipeline.query()

**Choice:** Add optional `conversation_history` parameter to `query()` method

**Rationale:**
- Keeps RAGPipeline as the main interface
- Allows other interfaces (web UI) to use conversation memory
- Maintains backward compatibility (parameter is optional)
- Clean separation of concerns

**Alternatives considered:**
- Pass directly to LLM: Bypasses pipeline abstraction
- Store in RAGPipeline state: Makes pipeline stateful, harder to test
- Global variable: Bad practice, not thread-safe

## Risks / Trade-offs

### Risk: Context window too large exceeds LLM limits
**Mitigation:**
- Default to conservative window size (5 turns)
- Document recommended limits in help text
- LLM's `truncate_context()` method already handles overflow
- Users can reduce window size if needed

### Risk: Conversation context confuses LLM with irrelevant history
**Trade-off accepted:**
- Users can disable by setting context_window to 0
- Most conversations benefit from context
- Alternative is to ask users to repeat context every time

### Risk: Long responses consume context window quickly
**Mitigation:**
- Use turn-based limit (not token-based) so long responses don't dominate
- Users can adjust window size based on their needs
- Consider adding response truncation in future if needed

### Risk: Conversation history not preserved in session files
**Mitigation:**
- Session files already store full conversation history
- No changes needed to session format
- Context window is rebuilt from history on load

### Risk: Performance impact from larger prompts
**Trade-off accepted:**
- Conversation context is small compared to document context
- 5 turns typically adds <1000 tokens
- Benefit of contextual responses outweighs minor latency increase

## Migration Plan

No migration needed - this is additive functionality.

Deployment steps:
1. Update `src/llm.py` to accept conversation history in `construct_prompt()`
2. Add `context_window` parameter to Config class
3. Add `get_context_window()` method to Session class
4. Update `src/rag.py` to pass conversation history to LLM
5. Update `terminal.py` to pass conversation history when querying
6. Add `/context` command handler
7. Update `/set` command to support `context_window`
8. Update README with conversation memory documentation

Rollback: Set `context_window` to 0 to disable conversation memory.

## Open Questions

1. **Should we show a visual indicator when conversation context is being used?**
   - Leaning yes: Brief message like "Using last 3 conversation turns for context"
   - Could be distracting, maybe only show in verbose mode

2. **Should conversation context be included in saved sessions?**
   - Already handled: session files store full history
   - Context window is rebuilt from history on load

3. **Should we add conversation summarization for very long sessions?**
   - Leaning no: Out of scope for this change
   - Users can /clear if conversation gets too long
   - Could add in future if requested
