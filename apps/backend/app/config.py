from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from pathlib import Path
import os

# Project root: multiagent ai/ai-voice-copilot
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = PROJECT_ROOT / "storage"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # API Keys (Free Tier)
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    cerebras_api_key: str = Field(default="", alias="CEREBRAS_API_KEY")
    ollama_base_url: str = Field(default="http://localhost:11434/v1", alias="OLLAMA_BASE_URL")

    # Mode defaults
    default_fast_provider: str = Field(default="groq", alias="DEFAULT_FAST_PROVIDER")
    default_fast_model: str = Field(default="llama-3.1-8b-instant", alias="DEFAULT_FAST_MODEL")

    default_reasoning_provider: str = Field(default="gemini", alias="DEFAULT_REASONING_PROVIDER")
    default_reasoning_model: str = Field(default="gemini-2.0-flash", alias="DEFAULT_REASONING_MODEL")

    default_research_provider: str = Field(default="groq", alias="DEFAULT_RESEARCH_PROVIDER")
    default_research_model: str = Field(default="llama-3.3-70b-versatile", alias="DEFAULT_RESEARCH_MODEL")

    enable_auto_routing: bool = Field(default=True, alias="ENABLE_AUTO_ROUTING")
    enable_fallback: bool = Field(default=True, alias="ENABLE_FALLBACK")
    llm_request_timeout_secs: int = Field(default=30, alias="LLM_REQUEST_TIMEOUT_SECS")

    # Audio & STT
    audio_capture_mode: str = Field(default="system", alias="AUDIO_CAPTURE_MODE")
    audio_sample_rate: int = Field(default=16000, alias="AUDIO_SAMPLE_RATE")
    grpc_host: str = Field(default="127.0.0.1", alias="GRPC_HOST")
    grpc_port: int = Field(default=50051, alias="GRPC_PORT")

    # Database & Storage (Robust absolute paths)
    project_root: Path = PROJECT_ROOT
    database_url: str = Field(
        default=f"sqlite+aiosqlite:///{STORAGE_DIR / 'database' / 'app.db'}",
        alias="DATABASE_URL"
    )
    vector_store_path: str = Field(
        default=str(STORAGE_DIR / "vector-store"),
        alias="VECTOR_STORE_PATH"
    )
    documents_original_path: str = Field(
        default=str(STORAGE_DIR / "documents" / "originals"),
        alias="DOCUMENTS_ORIGINAL_PATH"
    )
    documents_extracted_path: str = Field(
        default=str(STORAGE_DIR / "documents" / "extracted"),
        alias="DOCUMENTS_EXTRACTED_PATH"
    )
    embedding_model: str = Field(default="all-MiniLM-L6-v2", alias="EMBEDDING_MODEL")

    # Security
    secret_key: str = Field(default="change-this-to-a-random-secret-key", alias="SECRET_KEY")
    api_key_encryption_key: str = Field(
        default="wG5iN9qWcW9t6uW-4uK-5H5T4V_w5O-0Y8_Z9L8_M6c=",
        alias="API_KEY_ENCRYPTION_KEY"
    )

settings = Settings()
