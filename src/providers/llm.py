import requests

from src.config import settings
from src.providers.base import LLMProvider


class OllamaLLM(LLMProvider):
    def __init__(self, model=None, base_url=None):
        self.model = model or settings.llm_model
        self.base_url = base_url or settings.ollama_base_url

    def generate(self, prompt):
        resp = requests.post(
            f"{self.base_url}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["response"].strip()
