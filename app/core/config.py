from pydantic_settings import BaseSettings
from typing import Optional, ClassVar, Dict
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plataforma de Verificação de Fatos"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # MongoDB settings
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "fact_checker")
    
    # Social Media API Keys
    TWITTER_API_KEY: Optional[str] = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET: Optional[str] = os.getenv("TWITTER_API_SECRET")
    TWITTER_ACCESS_TOKEN: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_TOKEN_SECRET: Optional[str] = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
    
    # AI Model Settings
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models")
    CONFIDENCE_THRESHOLD: float = 0.85
    
    # Classification Labels
    CLASSIFICATION_LABELS: ClassVar[Dict[str, str]] = {
        "VERIFIED": "Verificado",
        "SUSPICIOUS": "Suspeito",
        "FAKE": "Falso"
    }
    
    class Config:
        case_sensitive = True

settings = Settings() 