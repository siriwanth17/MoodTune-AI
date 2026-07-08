from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "MoodTune AI"
    environment: str = "development"
    api_prefix: str = "/api"
    mongo_url: str = Field("mongodb://localhost:27017", alias="MONGO_URL")
    mongo_db: str = Field("moodtune_ai", alias="MONGO_DB")
    jwt_secret: str = Field("change-this-secret", alias="JWT_SECRET")
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60 * 24
    frontend_origin: str = Field("http://localhost:5173", alias="FRONTEND_ORIGIN")
    spotify_client_id: str | None = Field(None, alias="SPOTIFY_CLIENT_ID")
    spotify_client_secret: str | None = Field(None, alias="SPOTIFY_CLIENT_SECRET")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
