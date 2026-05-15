from src.embedder import Embedder
from src.vectorstore import VectorStore
from src.retriever import Retriever
from src.llm import OllamaLLM
from src.parser import DocumentParser
from src.chunker import Chunker
from pathlib import Path
from typing import List, Dict, Optional
import logging
import hashlib

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(
        self,
        persist_directory: str = "./storage/chroma",
        model_name: str = "llama3.1:8b",
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
        temperature: float = 0.7,
        max_tokens: int = 512
    ):
        logger.info("Initializing RAG pipeline...")

        self.embedder = Embedder()
        self.vectorstore = VectorStore(persist_directory=persist_directory)
        self.retriever = Retriever(
            embedder=self.embedder,
            vectorstore=self.vectorstore,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )
        self.llm = OllamaLLM(
            model=model_name,
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.parser = DocumentParser()
        self.chunker = Chunker(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )

        logger.info("RAG pipeline initialized")

    def _generate_doc_id(self, file_path: str, chunk_index: int) -> str:
        unique_string = f"{file_path}_{chunk_index}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def ingest_file(self, file_path: str) -> bool:
        logger.info(f"Ingesting file: {file_path}")

        if self.vectorstore.document_exists(file_path):
            logger.info(f"Document already exists, skipping: {file_path}")
            return False

        text = self.parser.parse(file_path)
        if not text:
            logger.error(f"Failed to parse file: {file_path}")
            return False

        chunks = self.chunker.chunk_text(text)
        if not chunks:
            logger.warning(f"No chunks generated for: {file_path}")
            return False

        logger.info(f"Generated {len(chunks)} chunks")

        embeddings = self.embedder.embed_batch(chunks, show_progress=False)

        ids = [self._generate_doc_id(file_path, i) for i in range(len(chunks))]
        metadatas = [
            {
                "source": file_path,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
            for i in range(len(chunks))
        ]

        self.vectorstore.add_documents(
            embeddings=embeddings.tolist(),
            texts=chunks,
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Successfully ingested: {file_path}")
        return True

    def ingest_directory(self, directory_path: str) -> Dict[str, int]:
        logger.info(f"Ingesting directory: {directory_path}")

        path = Path(directory_path)
        if not path.exists() or not path.is_dir():
            logger.error(f"Directory not found: {directory_path}")
            return {"success": 0, "failed": 0, "skipped": 0}

        supported_extensions = ['.pdf', '.txt', '.md', '.markdown']
        files = []
        for ext in supported_extensions:
            files.extend(path.rglob(f"*{ext}"))

        logger.info(f"Found {len(files)} files to process")

        stats = {"success": 0, "failed": 0, "skipped": 0}

        for file_path in files:
            try:
                result = self.ingest_file(str(file_path))
                if result:
                    stats["success"] += 1
                else:
                    stats["skipped"] += 1
            except Exception as e:
                logger.error(f"Error ingesting {file_path}: {e}")
                stats["failed"] += 1

        logger.info(f"Ingestion complete: {stats}")
        return stats

    def query(
        self,
        query: str,
        top_k: Optional[int] = None,
        similarity_threshold: Optional[float] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict:
        if self.vectorstore.get_document_count() == 0:
            return {
                "response": "No documents have been indexed yet. Please upload documents first.",
                "context_chunks": [],
                "error": "empty_database"
            }

        retrieved_chunks = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            similarity_threshold=similarity_threshold
        )

        if not retrieved_chunks:
            return {
                "response": "No relevant information found in the indexed documents.",
                "context_chunks": [],
                "error": "no_results"
            }

        prompt = self.llm.construct_prompt(query, retrieved_chunks)

        if stream:
            return {
                "stream": self.llm.generate(prompt, temperature, max_tokens, stream=True),
                "context_chunks": retrieved_chunks
            }
        else:
            result = self.llm.generate_response(prompt, temperature, max_tokens)
            result["context_chunks"] = retrieved_chunks
            return result

    def get_stats(self) -> Dict:
        return {
            "document_count": self.vectorstore.get_document_count(),
            "sources": self.vectorstore.get_all_sources()
        }

    def clear_database(self):
        logger.info("Clearing vector database...")
        self.vectorstore.clear()
        logger.info("Database cleared")
