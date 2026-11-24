import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "TRACEGRID"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    TEAM_NAME: str = "CyboShield"
    HACKATHON_TAG: str = "Rajasthan Police Hackathon 2026 - PS05"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./tracegrid.db")
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000"
    ]
    
    # Security & Limits
    MAX_UPLOAD_SIZE_MB: int = 25
    ALLOWED_EXTENSIONS: List[str] = ["csv", "xlsx"]
    
    # Optional LLM
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env", extra="ignore")

settings = Settings()
