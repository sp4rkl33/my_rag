"""Test script for conversation memory feature."""

import sys
import os
sys.path.insert(0, '.')

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')

from src.session import Session
from src.rag import RAGPipeline
from terminal import Config

def test_context_window():
    """Test Session.get_context_window() method."""
    print("Testing Session.get_context_window()...")

    session = Session()

    # Add some conversation history
    session.append("What is RAG?", "RAG stands for Retrieval-Augmented Generation...")
    session.append("How does it work?", "It works by retrieving relevant documents...")
    session.append("What are the benefits?", "The main benefits are accuracy and relevance...")
    session.append("Are there limitations?", "Yes, limitations include dependency on document quality...")
    session.append("Can you give examples?", "Examples include chatbots and Q&A systems...")

    # Test with different window sizes
    print("\n1. Get last 3 turns:")
    context = session.get_context_window(3)
    assert len(context) == 3
    print(f"   [OK] Got {len(context)} turns")

    print("\n2. Get last 5 turns:")
    context = session.get_context_window(5)
    assert len(context) == 5
    print(f"   [OK] Got {len(context)} turns")

    print("\n3. Get more turns than available (10):")
    context = session.get_context_window(10)
    assert len(context) == 5  # Should return all 5
    print(f"   [OK] Got {len(context)} turns (all available)")

    print("\n4. Get 0 turns (disabled):")
    context = session.get_context_window(0)
    assert len(context) == 0
    print(f"   [OK] Got {len(context)} turns (disabled)")

    print("\n[OK] All context window tests passed!")

def test_config_context_window():
    """Test Config.context_window parameter."""
    print("\nTesting Config.context_window parameter...")

    config = Config()

    # Test default value
    print("\n1. Default context_window:")
    assert config.context_window == 5
    print(f"   [OK] Default is {config.context_window}")

    # Test setting valid values
    print("\n2. Set context_window to 3:")
    config.validate_and_set("context_window", "3")
    assert config.context_window == 3
    print(f"   [OK] Set to {config.context_window}")

    print("\n3. Set context_window to 0 (disabled):")
    config.validate_and_set("context_window", "0")
    assert config.context_window == 0
    print(f"   [OK] Set to {config.context_window}")

    print("\n4. Set context_window to 10:")
    config.validate_and_set("context_window", "10")
    assert config.context_window == 10
    print(f"   [OK] Set to {config.context_window}")

    # Test invalid values
    print("\n5. Try setting negative value:")
    success, msg = config.validate_and_set("context_window", "-1")
    assert not success
    print(f"   [OK] Correctly rejected: {msg}")

    print("\n6. Check get_all() includes context_window:")
    all_config = config.get_all()
    assert "context_window" in all_config
    print(f"   [OK] context_window in config: {all_config['context_window']}")

    print("\n[OK] All config tests passed!")

def test_conversation_history_format():
    """Test conversation history formatting."""
    print("\nTesting conversation history formatting...")

    from src.llm import OllamaLLM

    llm = OllamaLLM()

    # Create sample conversation history
    conversation_history = [
        {"query": "What is RAG?", "response": "RAG stands for Retrieval-Augmented Generation."},
        {"query": "How does it work?", "response": "It retrieves relevant documents and generates responses."}
    ]

    # Test prompt construction with conversation history
    prompt = llm.construct_prompt(
        query="Can you give an example?",
        context_chunks=[{"text": "Example context about RAG systems..."}],
        conversation_history=conversation_history
    )

    # Verify conversation history is in the prompt
    assert "User: What is RAG?" in prompt
    assert "Assistant: RAG stands for Retrieval-Augmented Generation." in prompt
    assert "User: How does it work?" in prompt
    assert "Assistant: It retrieves relevant documents and generates responses." in prompt
    assert "Question: Can you give an example?" in prompt

    print("   [OK] Conversation history correctly formatted in prompt")

    # Test without conversation history
    prompt_no_history = llm.construct_prompt(
        query="What is RAG?",
        context_chunks=[{"text": "Context about RAG..."}],
        conversation_history=None
    )

    assert "User:" not in prompt_no_history
    assert "Assistant:" not in prompt_no_history
    print("   [OK] Prompt without conversation history works correctly")

    print("\n[OK] All conversation history formatting tests passed!")

def test_session_persistence():
    """Test that conversation context persists after save/load."""
    print("\nTesting session persistence with conversation context...")

    session = Session()

    # Add conversation history
    session.append("What is machine learning?", "Machine learning is a subset of AI...")
    session.append("What are its types?", "The main types are supervised, unsupervised...")
    session.append("Can you explain supervised learning?", "Supervised learning uses labeled data...")

    # Get context before save
    context_before = session.get_context_window(3)
    assert len(context_before) == 3
    print(f"   [OK] Context before save: {len(context_before)} turns")

    # Save session
    filename = "test_session_memory"
    success = session.save_to_file(filename)
    assert success
    print(f"   [OK] Session saved")

    # Create new session and load
    new_session = Session()
    success = new_session.load_from_file(filename)
    assert success
    print(f"   [OK] Session loaded")

    # Get context after load
    context_after = new_session.get_context_window(3)
    assert len(context_after) == 3
    print(f"   [OK] Context after load: {len(context_after)} turns")

    # Verify content matches
    for i in range(3):
        assert context_before[i]["query"] == context_after[i]["query"]
        assert context_before[i]["response"] == context_after[i]["response"]

    print("   [OK] Context content matches after save/load")
    print("\n[OK] Session persistence test passed!")

def test_clear_clears_context():
    """Test that /clear command clears conversation context."""
    print("\nTesting that clear() clears conversation context...")

    session = Session()

    # Add conversation history
    session.append("Question 1", "Answer 1")
    session.append("Question 2", "Answer 2")
    session.append("Question 3", "Answer 3")

    context_before = session.get_context_window(5)
    assert len(context_before) == 3
    print(f"   [OK] Context before clear: {len(context_before)} turns")

    # Clear session
    session.clear()

    context_after = session.get_context_window(5)
    assert len(context_after) == 0
    print(f"   [OK] Context after clear: {len(context_after)} turns")

    print("\n[OK] Clear test passed!")

if __name__ == "__main__":
    print("=" * 70)
    print("CONVERSATION MEMORY FEATURE TESTS")
    print("=" * 70)

    try:
        test_context_window()
        test_config_context_window()
        test_conversation_history_format()
        test_session_persistence()
        test_clear_clears_context()

        print("\n" + "=" * 70)
        print("ALL TESTS PASSED [OK]")
        print("=" * 70)

    except AssertionError as e:
        print(f"\n[FAIL] Test failed: {e}")
        exit(1)
    except Exception as e:
        print(f"\n[FAIL] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
