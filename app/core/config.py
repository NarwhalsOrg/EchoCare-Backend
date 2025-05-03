import os
from dotenv import load_dotenv

load_dotenv()




class DevSettings:
    # For SQLite, you don't need host, port, user, or password
    DB_NAME: str = "./DemoDB/diabetes_db.sqlite3"
    DATABASE_URL = f"sqlite:///{DB_NAME}"

    JWT_SECRET: str = os.getenv("JWT_SECRET") or "your_super_secret_key"
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM") or "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60)

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or ""

    ENV: str = os.getenv("ENV") or "development"




# Deploy Config
# Load environment variables from .env file
class Settings:
    DB_HOST: str = os.getenv("DB_HOST") or "localhost"
    DB_PORT: int = int(os.getenv("DB_PORT") or 3306)
    DB_USER: str = os.getenv("DB_USER") or "root"
    DB_PASSWORD: str = os.getenv("DB_PASSWORD") or ""
    DB_NAME: str = os.getenv("DB_NAME") or "diabetes_db"
    DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    JWT_SECRET: str = os.getenv("JWT_SECRET") or "your_super_secret_key"
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM") or "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or 60)

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY") or ""

    ENV: str = os.getenv("ENV") or "development"




# Load environment variables from .env file
# Check if the environment is development or production
# settings = Settings()


# Load for development
# UNCOMMENT THIS LINE FOR DEVELOPMENT
settings = DevSettings()
