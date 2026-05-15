import chromadb
from chromadb.config import Settings
from typing import List, Dict, Optional
import os


class VectorStore:
    def __init__(self, persist_directory: str = "./storage/chroma"):
        self.persist_directory = persist_directory
        os.makedirs(persist_directory, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=persist_directory,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )

        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(
        self,
        embeddings: List[List[float]],
        texts: List[str],
        metadatas: List[Dict],
        ids: List[str]
    ):
        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids
        )

    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5,
        where: Optional[Dict] = None
    ) -> Dict:
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"]
        )
        return results

    def get_document_count(self) -> int:
        return self.collection.count()

    def get_all_sources(self) -> List[str]:
        all_docs = self.collection.get(include=["metadatas"])
        sources = set()
        if all_docs and all_docs.get("metadatas"):
            for metadata in all_docs["metadatas"]:
                if "source" in metadata:
                    sources.add(metadata["source"])
        return sorted(list(sources))

    def document_exists(self, source: str) -> bool:
        results = self.collection.get(
            where={"source": source},
            limit=1
        )
        return len(results["ids"]) > 0

    def clear(self):
        self.client.delete_collection("documents")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
