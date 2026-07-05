from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "gemma2:latest"
    upload_dir: str = "temp_uploads"
    chroma_dir: str = "chroma_db"
    chunk_size: int = 1000
    chunk_overlap: int = 200
    model_name: str = "all-MiniLM-L6-v2"

    model_config = {"env_prefix": "KB_"}

settings = Settings()
