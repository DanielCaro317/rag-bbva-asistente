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


class OpenAICompatLLM(LLMProvider):
    # sirve para Groq, OpenRouter, OpenAI... (misma API de chat completions)
    def __init__(self, model=None, base_url=None, api_key=None):
        self.model = model or settings.llm_model
        self.base_url = base_url or settings.llm_api_base
        self.api_key = api_key or settings.llm_api_key

    def generate(self, prompt):
        resp = requests.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
            },
            timeout=120,
        )
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"].strip()
