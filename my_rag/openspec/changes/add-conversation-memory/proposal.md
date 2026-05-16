## Why

The terminal RAG app currently treats each query independently without maintaining conversation context. Users cannot ask follow-up questions or have natural conversations because the AI doesn't remember previous exchanges. This makes the experience feel disconnected and requires users to repeat context in every query.

## What Changes

- Add conversation history tracking to maintain context across queries
- Modify LLM prompt construction to include recent conversation turns
- Add configurable conversation window size to control context length
- Update terminal UI to show conversation context being used
- Add `/context` command to view current conversation context
- Add option to toggle conversation memory on/off

## Capabilities

### New Capabilities
- `conversation-context`: Track and include conversation history in LLM prompts for contextual responses

### Modified Capabilities
<!-- No existing capabilities are being modified -->

## Impact

**Modified Files:**
- `src/llm.py`: Update `construct_prompt()` to accept and include conversation history
- `terminal.py`: Pass conversation history from session to LLM when querying
- `src/session.py`: Add method to get recent conversation turns for context

**New Features:**
- Conversation memory enabled by default
- Configurable context window (default: last 5 turns)
- `/context` command to view current conversation context
- `/set context_window <n>` to adjust how many turns to remember

**User Experience:**
- Users can ask follow-up questions naturally
- AI remembers previous answers and can reference them
- More natural conversational flow
- No breaking changes - existing functionality preserved
