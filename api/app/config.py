from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://happyrobot:happyrobot@postgres:5432/happyrobot"
    api_key: str = "demo-key-change-me"
    fmcsa_api_url: str = "https://mobile.fmcsa.dot.gov/qc/services/carriers/"
    fmcsa_api_key: str = ""
    cors_origins: str = "http://localhost:5173"
    log_level: str = "info"
    happyrobot_api_key: str = ""
    happyrobot_base_url: str = "https://platform.happyrobot.ai/api/v2"
    workflow_id: str = ""
    dashboard_password: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"

    @field_validator("database_url", mode="before")
    @classmethod
    def fix_postgres_scheme(cls, v):
        """Fly's 'fly postgres attach' generates postgres:// URLs.
        SQLAlchemy requires 'postgresql://' — normalize it here."""
        if isinstance(v, str) and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        if isinstance(v, str) and v.startswith("postgres+asyncpg://"):
            return v.replace("postgres+asyncpg://", "postgresql+asyncpg://", 1)
        return v

    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

@lru_cache()
def get_settings() -> Settings:
    return Settings()
