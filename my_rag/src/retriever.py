from typing import List, Dict, Optional
from src.embedder import Embedder
from src.vectorstore import VectorStore


class Retriever:
    def __init__(
        self,
        embedder: Embedder,
        vectorstore: VectorStore,
        top_k: int = 5,
        similarity_threshold: float = 0.3
    ):
        self.embedder = embedder
        self.vectorstore = vectorstore
        self.top_k = top_k
        self.similarity_threshold = similarity_threshold

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None
    ) -> List[Dict]:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        k = top_k if top_k is not None else self.top_k
        threshold = similarity_threshold if similarity_threshold is not None else self.similarity_threshold

        query_embedding = self.embedder.embed(query)

        results = self.vectorstore.query(
            query_embedding=query_embedding.tolist(),
            n_results=k
        )

        formatted_results = []
        if results and results.get("documents") and len(results["documents"]) > 0:
            documents = results["documents"][0]
            metadatas = results["metadatas"][0]
            distances = results["distances"][0]

            for doc, metadata, distance in zip(documents, metadatas, distances):
                similarity_score = 1 - distance

                if similarity_score >= threshold:
                    formatted_results.append({
                        "text": doc,
                        "source": metadata.get("source", "unknown"),
                        "chunk_index": metadata.get("chunk_index", 0),
                        "similarity_score": similarity_score
                    })

        formatted_results.sort(key=lambda x: x["similarity_score"], reverse=True)

        return formatted_results
