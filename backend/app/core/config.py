"""
Application configuration
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # Environment
    ENVIRONMENT: str = "local"

    # Database
    SYNAPSE_CONNECTION_STRING: str
    APP_DB_URL: str

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # JWT
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 15

    # OAuth
    GOOGLE_ADS_CLIENT_ID: str = ""
    GOOGLE_ADS_CLIENT_SECRET: str = ""
    META_APP_ID: str = ""
    META_APP_SECRET: str = ""

    # Feature flags
    USE_MOCKED_OAUTH: bool = False
    USE_MOCKED_APIS: bool = False

    class Config:
        env_file = ".env.local"
        case_sensitive = True


settings = Settings()
