import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Keys
    google_factcheck_api_key: str = os.getenv("GOOGLE_FACTCHECK_API_KEY", "")
    news_api_key: str = os.getenv("NEWS_API_KEY", "")
    huggingface_token: str = os.getenv("HUGGINGFACE_TOKEN", "")
    kaggle_api_token: str = os.getenv("KAGGLE_API_TOKEN", "")

    # Supabase
    supabase_url: str = os.getenv("SUPABASE_URL", "https://vhknnhducrjpgjfvxsqf.supabase.co")
    supabase_key: str = os.getenv("SUPABASE_KEY", "")

    # Server
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "true").lower() == "true"

    # Model
    classifier_model: str = "roberta-base"
    max_claims: int = 10

    # Trusted Sources
    trusted_domains: list[str] = [
        "snopes.com",
        "reuters.com",
        "factcheck.org",
        "politifact.com",
        "apnews.com",
        "bbc.com",
        "nasa.gov",
        "who.int",
        "cdc.gov",
        "nature.com",
        "science.org",
        "scholar.google.com",
    ]

    class Config:
        env_file = ".env"


settings = Settings()
