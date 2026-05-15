from src.llm import OllamaLLM

print("Testing Ollama LLM Integration...")
print("=" * 50)

print("\n1. Initializing Ollama client...")
llm = OllamaLLM(model="llama3.1:8b")

print("\n2. Checking if Ollama is running...")
if not llm.is_running():
    print("❌ ERROR: Ollama is not running!")
    print("\nPlease start Ollama with: ollama serve")
    print("Then run this test again.")
    exit(1)
print("✓ Ollama is running")

print("\n3. Checking if model is available...")
if not llm.model_exists():
    print(f"❌ ERROR: Model '{llm.model}' not found!")
    print(f"\nPlease pull the model with: ollama pull {llm.model}")
    print("Or use a different model like: phi3:mini")
    exit(1)
print(f"✓ Model '{llm.model}' is available")

print("\n4. Testing prompt construction...")
sample_context = [
    {
        "text": "Python is a high-level programming language.",
        "source": "test.txt",
        "chunk_index": 0
    },
    {
        "text": "It is known for its simplicity and readability.",
        "source": "test.txt",
        "chunk_index": 1
    }
]
query = "What is Python?"
prompt = llm.construct_prompt(query, sample_context)
print(f"✓ Constructed prompt ({len(prompt)} characters)")

print("\n5. Testing streaming generation...")
print(f"Query: '{query}'")
print("\nStreaming response:")
print("-" * 50)

try:
    for chunk in llm.generate(prompt, temperature=0.7, max_tokens=100, stream=True):
        print(chunk, end="", flush=True)
    print("\n" + "-" * 50)
    print("✓ Streaming generation successful")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    exit(1)

print("\n6. Testing full response generation with metadata...")
test_prompt = "Explain what Python is in one sentence."
try:
    result = llm.generate_response(test_prompt, temperature=0.7, max_tokens=50)
    print(f"Response: {result['response'][:100]}...")
    print(f"Token count: {result['token_count']}")
    print(f"Generation time: {result['generation_time']:.2f}s")
    print(f"Model: {result['model']}")
    print("✓ Full response generation successful")
except Exception as e:
    print(f"❌ ERROR: {e}")
    exit(1)

print("\n7. Testing with no context...")
prompt_no_context = llm.construct_prompt("What is the capital of France?", [])
print("✓ Prompt construction with no context works")

print("\n" + "=" * 50)
print("LLM integration test complete!")
print("\nNote: If you see this message, Ollama is working correctly.")
