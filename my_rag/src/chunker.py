import re
from typing import List
import tiktoken


class Chunker:
    def __init__(
        self,
        chunk_size: int = 800,
        chunk_overlap: int = 100,
        encoding_name: str = "cl100k_base"
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.encoding = tiktoken.get_encoding(encoding_name)

    def count_tokens(self, text: str) -> int:
        return len(self.encoding.encode(text))

    def split_into_sentences(self, text: str) -> List[str]:
        sentence_endings = re.compile(r'(?<=[.!?])\s+')
        sentences = sentence_endings.split(text)
        return [s.strip() for s in sentences if s.strip()]

    def chunk_text(self, text: str) -> List[str]:
        if not text or not text.strip():
            return []

        total_tokens = self.count_tokens(text)

        if total_tokens <= self.chunk_size:
            return [text]

        sentences = self.split_into_sentences(text)

        if not sentences:
            return self._chunk_by_characters(text)

        chunks = []
        current_chunk = []
        current_tokens = 0

        for sentence in sentences:
            sentence_tokens = self.count_tokens(sentence)

            if sentence_tokens > self.chunk_size:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))
                    current_chunk = []
                    current_tokens = 0

                chunks.extend(self._chunk_by_characters(sentence))
                continue

            if current_tokens + sentence_tokens <= self.chunk_size:
                current_chunk.append(sentence)
                current_tokens += sentence_tokens
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                overlap_chunk = []
                overlap_tokens = 0
                for s in reversed(current_chunk):
                    s_tokens = self.count_tokens(s)
                    if overlap_tokens + s_tokens <= self.chunk_overlap:
                        overlap_chunk.insert(0, s)
                        overlap_tokens += s_tokens
                    else:
                        break

                current_chunk = overlap_chunk + [sentence]
                current_tokens = overlap_tokens + sentence_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks

    def _chunk_by_characters(self, text: str) -> List[str]:
        words = text.split()
        chunks = []
        current_chunk = []
        current_tokens = 0

        for word in words:
            word_tokens = self.count_tokens(word + " ")

            if current_tokens + word_tokens <= self.chunk_size:
                current_chunk.append(word)
                current_tokens += word_tokens
            else:
                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                overlap_words = []
                overlap_tokens = 0
                for w in reversed(current_chunk):
                    w_tokens = self.count_tokens(w + " ")
                    if overlap_tokens + w_tokens <= self.chunk_overlap:
                        overlap_words.insert(0, w)
                        overlap_tokens += w_tokens
                    else:
                        break

                current_chunk = overlap_words + [word]
                current_tokens = overlap_tokens + word_tokens

        if current_chunk:
            chunks.append(" ".join(current_chunk))

        return chunks
