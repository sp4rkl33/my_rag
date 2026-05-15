import requests
from typing import Dict, List, Optional, Iterator
import time
import json


class OllamaLLM:
    def __init__(
        self,
        base_url: str = "http://localhost:11434",
        model: str = "llama3.1:8b",
        temperature: float = 0.7,
        max_tokens: int = 512
    ):
        self.base_url = base_url
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens

    def is_running(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def model_exists(self, model_name: Optional[str] = None) -> bool:
        model = model_name or self.model
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(m.get("name") == model for m in models)
            return False
        except requests.exceptions.RequestException:
            return False

    def construct_prompt(
        self,
        query: str,
        context_chunks: List[Dict],
        system_instruction: Optional[str] = None
    ) -> str:
        if system_instruction is None:
            system_instruction = (
                "You are a helpful assistant that answers questions based on the provided context. "
                "Use the context to provide accurate, relevant answers. "
                "If the context doesn't contain enough information, say so."
            )

        if not context_chunks:
            prompt = f"{system_instruction}\n\nNo relevant context was found.\n\nQuestion: {query}\n\nAnswer:"
        else:
            context_text = "\n\n".join([
                f"[Source: {chunk['source']}, Chunk {chunk['chunk_index']}]\n{chunk['text']}"
                for chunk in context_chunks
            ])

            prompt = f"{system_instruction}\n\nContext:\n{context_text}\n\nQuestion: {query}\n\nAnswer:"

        return prompt

    def truncate_context(self, prompt: str, max_tokens: int = 8192) -> str:
        approx_tokens = len(prompt.split())
        if approx_tokens <= max_tokens:
            return prompt

        words = prompt.split()
        truncated = " ".join(words[:max_tokens])
        return truncated + "\n\n[Context truncated due to length...]"

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = True
    ) -> Iterator[str]:
        temp = temperature if temperature is not None else self.temperature
        max_tok = max_tokens if max_tokens is not None else self.max_tokens

        truncated_prompt = self.truncate_context(prompt)

        payload = {
            "model": self.model,
            "prompt": truncated_prompt,
            "stream": stream,
            "options": {
                "temperature": temp,
                "num_predict": max_tok
            }
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=stream,
                timeout=300
            )
            response.raise_for_status()

            if stream:
                for line in response.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if "response" in chunk:
                            yield chunk["response"]
            else:
                result = response.json()
                yield result.get("response", "")

        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Ollama generation failed: {str(e)}")

    def generate_response(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict:
        start_time = time.time()
        full_response = ""
        token_count = 0

        try:
            for chunk in self.generate(prompt, temperature, max_tokens, stream=True):
                full_response += chunk
                token_count += 1

            generation_time = time.time() - start_time

            return {
                "response": full_response,
                "token_count": token_count,
                "generation_time": generation_time,
                "model": self.model
            }

        except Exception as e:
            raise RuntimeError(f"Response generation failed: {str(e)}")
