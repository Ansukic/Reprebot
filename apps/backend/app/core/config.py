from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    groq_api_key: str
    groq_chat_model: str = "openai/gpt-oss-120b"
    groq_base_url: str = "https://api.groq.com/openai/v1"

    embeddings_model: str = "jinaai/jina-embeddings-v2-base-es"
    embeddings_dim: int = 768

    data_dir: str = "data"
    cors_origins: str = "*"
    admin_token: str = ""

    top_k: int = 5
    chunk_size: int = 1000
    chunk_overlap: int = 150

    @property
    def cors_origins_list(self) -> list[str]:
        if self.cors_origins.strip() == "*":
            return ["*"]
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
