from typing import List
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Healthcare API"
    API_V1_STR: str = "/api"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[AnyHttpUrl]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # JWT
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "supersecretkey")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Supabase
    SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY: str = os.getenv("SUPABASE_KEY", "")
    SUPABASE_BUCKET_AVATARS: str = "avatars"
    SUPABASE_BUCKET_PRESCRIPTIONS: str = "prescriptions"

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()