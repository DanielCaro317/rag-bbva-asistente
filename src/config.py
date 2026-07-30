from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"

    llm_provider: str = "ollama"
    llm_model: str = "qwen2.5:3b"
    ollama_base_url: str = "http://ollama:11434"

    embeddings_model: str = "intfloat/multilingual-e5-base"

    vector_store: str = "qdrant"
    qdrant_url: str = "http://qdrant:6333"
    collection_name: str = "bbva"

    chunk_size: int = 800
    chunk_overlap: int = 120
    top_k: int = 5
    reranker_enabled: bool = True
    reranker_model: str = "BAAI/bge-reranker-v2-m3"

    history_n: int = 6
    db_path: str = "data/conversations.sqlite3"

    scraper_base_url: str = "https://www.scotiabankcolpatria.com/"
    scraper_max_pages: int = 50


settings = Settings()
