from functools import lru_cache
from pathlib import Path
import os
from pydantic import BaseModel


class Settings(BaseModel):
    project_root: Path = Path(__file__).resolve().parents[2]
    llm_provider: str = "mock"
    llm_model: str = ""
    groq_api_key: str = ""
    ollama_url: str = "http://127.0.0.1:11434"
    qdrant_url: str = "http://localhost:6333"
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L-6-v2"
    top_k_dense: int = 20
    top_k_bm25: int = 20
    top_k_rerank: int = 6
    rrf_k: int = 60
    include_synthetic_corpus: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings(
        project_root=Path(os.getenv("PROJECT_ROOT", Path(__file__).resolve().parents[2])),
        llm_provider=os.getenv("LLM_PROVIDER", "auto"),
        llm_model=os.getenv("LLM_MODEL", ""),
        groq_api_key=os.getenv("GROQ_API_KEY", ""),
        ollama_url=os.getenv("OLLAMA_URL", "http://127.0.0.1:11434"),
        qdrant_url=os.getenv("QDRANT_URL", "http://localhost:6333"),
        include_synthetic_corpus=os.getenv("INCLUDE_SYNTHETIC_CORPUS", "false").lower() in {"1", "true", "yes"},
    )
