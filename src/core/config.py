import os
from logging import config as logging_config
from dotenv import load_dotenv
from src.core.logger import LOGGING
from starlette.config import Config

load_dotenv()

logging_config.dictConfig(LOGGING)

config = Config(".env")

# Project settings
PROJECT_NAME: str = config("PROJECT_NAME", default="fastapi-starter")
PROJECT_HOST: str = config("PROJECT_HOST", default="127.0.0.1")
PROJECT_PORT: int = config("PROJECT_PORT", cast=int, default=8000)

# Database settings
POSTGRES_USER: str = config("POSTGRES_USER", default="postgres")
POSTGRES_PASSWORD: str = config("POSTGRES_PASSWORD", default="postgres")
POSTGRES_SERVER: str = config("POSTGRES_SERVER", default="localhost")
POSTGRES_PORT: int = config("POSTGRES_PORT", cast=int, default=5432)
POSTGRES_DB: str = config("POSTGRES_DB", default="fastapi_starter")
DATABASE_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Security settings
SECRET_KEY: str = config("SECRET_KEY", default="your-very-secret-and-long-key-that-is-hard-to-guess-at-least-32-characters")
ACCESS_TOKEN_EXPIRE_MINUTES: int = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60 * 24 * 30)  # 30 days
ALGORITHM: str = "HS256"
