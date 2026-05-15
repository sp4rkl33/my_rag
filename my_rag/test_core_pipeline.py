from src.embedder import Embedder
from src.vectorstore import VectorStore
from src.retriever import Retriever

print("Testing Core RAG Pipeline...")
print("=" * 50)

print("\n1. Initializing components...")
embedder = Embedder()
vectorstore = VectorStore(persist_directory="./storage/chroma_test")
retriever = Retriever(embedder, vectorstore, top_k=3, similarity_threshold=0.2)

print("\n2. Creating sample documents...")
sample_docs = [
    "Python is a high-level programming language known for its simplicity and readability.",
    "Machine learning is a subset of artificial intelligence that focuses on data and algorithms.",
    "Natural language processing enables computers to understand and generate human language.",
    "Vector databases store data as high-dimensional vectors for similarity search.",
    "RAG systems combine retrieval and generation to produce contextual responses."
]

print("\n3. Generating embeddings...")
embeddings = embedder.embed_batch(sample_docs, show_progress=True)
print(f"Generated {len(embeddings)} embeddings with dimension {embeddings.shape[1]}")

print("\n4. Storing in ChromaDB...")
ids = [f"doc_{i}" for i in range(len(sample_docs))]
metadatas = [{"source": "test_doc.txt", "chunk_index": i} for i in range(len(sample_docs))]
vectorstore.add_documents(
    embeddings=embeddings.tolist(),
    texts=sample_docs,
    metadatas=metadatas,
    ids=ids
)
print(f"Stored {vectorstore.get_document_count()} documents")

print("\n5. Testing retrieval...")
query = "What is machine learning?"
print(f"Query: '{query}'")
results = retriever.retrieve(query, top_k=3)

print(f"\nFound {len(results)} relevant chunks:")
for i, result in enumerate(results, 1):
    print(f"\n  Result {i}:")
    print(f"    Text: {result['text'][:80]}...")
    print(f"    Source: {result['source']}")
    print(f"    Chunk Index: {result['chunk_index']}")
    print(f"    Similarity: {result['similarity_score']:.3f}")

print("\n6. Testing with different query...")
query2 = "How do vector databases work?"
print(f"Query: '{query2}'")
results2 = retriever.retrieve(query2, top_k=2)

print(f"\nFound {len(results2)} relevant chunks:")
for i, result in enumerate(results2, 1):
    print(f"\n  Result {i}:")
    print(f"    Text: {result['text'][:80]}...")
    print(f"    Similarity: {result['similarity_score']:.3f}")

print("\n" + "=" * 50)
print("Core pipeline test complete!")
print("\nCleaning up test database...")
vectorstore.clear()
print("Done!")
