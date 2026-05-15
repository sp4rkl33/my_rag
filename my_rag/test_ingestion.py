from src.rag import RAGPipeline
from pathlib import Path

print("Testing Document Ingestion...")
print("=" * 50)

print("\n1. Creating sample documents...")
sample_dir = Path("./data/documents/samples")
sample_dir.mkdir(parents=True, exist_ok=True)

sample_texts = {
    "python_intro.txt": """Python is a high-level, interpreted programming language known for its simplicity and readability.
It was created by Guido van Rossum and first released in 1991.
Python supports multiple programming paradigms including procedural, object-oriented, and functional programming.
It has a comprehensive standard library and a large ecosystem of third-party packages.""",

    "machine_learning.txt": """Machine learning is a subset of artificial intelligence that focuses on building systems that learn from data.
Instead of being explicitly programmed, these systems improve their performance through experience.
Common machine learning algorithms include linear regression, decision trees, neural networks, and support vector machines.
Applications range from image recognition to natural language processing.""",

    "rag_systems.md": """# Retrieval-Augmented Generation (RAG)

RAG is an AI framework that combines information retrieval with text generation.

## How it works:
1. Documents are split into chunks and embedded as vectors
2. User queries are embedded using the same model
3. Similar chunks are retrieved via vector search
4. Retrieved context is provided to an LLM for response generation

## Benefits:
- Grounds responses in factual information
- Reduces hallucinations
- Allows updating knowledge without retraining"""
}

for filename, content in sample_texts.items():
    file_path = sample_dir / filename
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  Created: {filename}")

print("\n2. Initializing RAG pipeline...")
rag = RAGPipeline(persist_directory="./storage/chroma_test")

print("\n3. Ingesting sample documents...")
stats = rag.ingest_directory(str(sample_dir))
print(f"  Success: {stats['success']}")
print(f"  Skipped: {stats['skipped']}")
print(f"  Failed: {stats['failed']}")

print("\n4. Verifying database...")
db_stats = rag.get_stats()
print(f"  Total chunks: {db_stats['document_count']}")
print(f"  Unique sources: {len(db_stats['sources'])}")
print(f"  Sources:")
for source in db_stats['sources']:
    print(f"    - {Path(source).name}")

print("\n5. Testing retrieval...")
test_query = "What is Python?"
print(f"  Query: '{test_query}'")
results = rag.retriever.retrieve(test_query, top_k=3)
print(f"  Retrieved {len(results)} chunks:")
for i, result in enumerate(results, 1):
    print(f"\n    Chunk {i}:")
    print(f"      Text: {result['text'][:80]}...")
    print(f"      Source: {Path(result['source']).name}")
    print(f"      Similarity: {result['similarity_score']:.3f}")

print("\n6. Testing re-ingestion (should skip duplicates)...")
stats2 = rag.ingest_directory(str(sample_dir))
print(f"  Success: {stats2['success']}")
print(f"  Skipped: {stats2['skipped']} (should be 3)")

print("\n" + "=" * 50)
print("Ingestion test complete!")
print("\nCleaning up test database...")
rag.clear_database()
print("Done!")
