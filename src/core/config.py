"""Define the application and database configuration settings."""

from functools import lru_cache
from typing import ClassVar, Literal

from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    """Define general application metadata and runtime settings."""

    name: str = "Clinicore API"
    description: str = """
        Clinicore API is a backend service that provides a set of endpoints for 
        managing and accessing clinic-related data. It is designed to be fast, 
        secure, and scalable, making it suitable for use in healthcare applications.
    """
    version: str = "0.1.0"
    env: Literal["development", "testing", "production"] = "development"
    debug: bool = False


class DatabaseSettings(BaseModel):
    """Define database connection settings."""

    host: str
    port: int
    name: str
    user: str
    password: SecretStr

    @property
    def url(self) -> str:
        """Return the asynchronous database connection URL."""
        return (
            f"postgresql+asyncpg://"
            f"{self.user}:{self.password.get_secret_value()}"
            f"@{self.host}:{self.port}/{self.name}"
        )


class Settings(BaseSettings):
    """Define the application settings loaded from the environment."""

    app: AppSettings = AppSettings()
    database: DatabaseSettings

    jwt_secret_key: SecretStr
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_nested_delimiter="__"
    )


@lru_cache
def get_settings() -> Settings:
    """Return the cached application settings instance."""
    return Settings()  # pyright: ignore[reportCallIssue]


settings = get_settings()
