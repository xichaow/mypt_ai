from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    openai_api_key: Optional[str] = None
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_origins: List[str] = ["*"]
    
    # Production settings
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    @property
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()