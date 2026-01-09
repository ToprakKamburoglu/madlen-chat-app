from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # App Info
    APP_NAME: str = "Madlen AI Chat"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # OpenRouter
    OPENROUTER_API_KEY: str
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    
    # Database
    DATABASE_URL: str = "sqlite:///./chat.db"
    
    # CORS
    CORS_ORIGINS: str = '["http://localhost:5173","http://127.0.0.1:5173"]'
    
    # OpenTelemetry / Jaeger
    JAEGER_ENDPOINT: str = "http://localhost:4317"
    OTEL_SERVICE_NAME: str = "madlen-chat-backend"
    ENABLE_TRACING: bool = True
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins from string to list"""
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:5173", "http://127.0.0.1:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
