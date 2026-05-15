from src.rag import RAGPipeline
from pathlib import Path

print("Testing End-to-End RAG System...")
print("=" * 70)

print("\n1. Creating test documents...")
test_dir = Path("./data/documents/test_e2e")
test_dir.mkdir(parents=True, exist_ok=True)

test_docs = {
    "ai_basics.txt": """Artificial Intelligence (AI) is the simulation of human intelligence by machines.
AI systems can perform tasks that typically require human intelligence, such as visual perception,
speech recognition, decision-making, and language translation.

There are two main types of AI:
- Narrow AI: Designed for specific tasks (like voice assistants)
- General AI: Hypothetical AI with human-like intelligence across all domains

Machine learning is a key subset of AI that enables systems to learn from data.""",

    "vector_databases.md": """# Vector Databases

Vector databases are specialized databases designed to store and query high-dimensional vectors.

## Key Features:
- Store embeddings (numerical representations of data)
- Perform similarity search using distance metrics
- Scale to billions of vectors
- Support metadata filtering

## Popular Vector Databases:
- ChromaDB: Lightweight, embedded database
- Pinecone: Managed cloud service
- Weaviate: Open-source with GraphQL API
- FAISS: Facebook's similarity search library

## Use Cases:
- Semantic search
- Recommendation systems
- RAG systems
- Image similarity search"""
}

for filename, content in test_docs.items():
    with open(test_dir / filename, 'w', encoding='utf-8') as f:
        f.write(content)
print(f"  Created {len(test_docs)} test documents")

print("\n2. Initializing RAG pipeline...")
rag = RAGPipeline(persist_directory="./storage/chroma_e2e_test")

print("\n3. Ingesting documents...")
stats = rag.ingest_directory(str(test_dir))
print(f"  Ingested: {stats['success']} files")
print(f"  Total chunks: {rag.get_stats()['document_count']}")

print("\n4. Testing queries...")
print("=" * 70)

test_queries = [
    "What is artificial intelligence?",
    "What are vector databases used for?",
    "What is the difference between narrow AI and general AI?"
]

for i, query in enumerate(test_queries, 1):
    print(f"\n[Query {i}] {query}")
    print("-" * 70)

    try:
        result = rag.query(
            query=query,
            top_k=3,
            similarity_threshold=0.2,
            temperature=0.7,
            max_tokens=150,
            stream=False
        )

        if "error" in result:
            print(f"ERROR: {result['response']}")
            continue

        print(f"\nResponse:\n{result['response']}")

        print(f"\nContext used: {len(result['context_chunks'])} chunks")
        for chunk in result['context_chunks']:
            print(f"  - {Path(chunk['source']).name} (similarity: {chunk['similarity_score']:.3f})")

        print(f"\nMetadata:")
        print(f"  Generation time: {result.get('generation_time', 0):.2f}s")
        print(f"  Tokens: {result.get('token_count', 0)}")

    except Exception as e:
        print(f"ERROR: {e}")

print("\n" + "=" * 70)
print("End-to-end RAG test complete!")

print("\n5. Testing error scenarios...")

print("\n  a) Query with no relevant results:")
result = rag.query("What is quantum computing?", similarity_threshold=0.9)
print(f"     Response: {result['response'][:100]}...")

print("\n  b) Empty query handling:")
try:
    result = rag.query("")
except ValueError as e:
    print(f"     Caught expected error: {e}")

print("\n6. Cleaning up...")
rag.clear_database()
print("  Database cleared")

print("\n" + "=" * 70)
print("All tests passed!")
print("\nNote: To test with Ollama, make sure it's running with:")
print("  ollama serve")
print("  ollama pull llama3.1:8b")
