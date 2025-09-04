from pydantic import BaseSettings
from dotenv import load_dotenv
import os

# Load from .env at project root
load_dotenv()

class Settings(BaseSettings):
    app_name: str = os.getenv("APP_NAME")
    app_env: str = os.getenv("APP_ENV")
    debug: bool = os.getenv("APP_DEBUG", "False") == "True"

    database_url: str = os.getenv("DATABASE_URL")

    secret_key: str = os.getenv("SECRET_KEY")
    algorithm: str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

settings = Settings()

