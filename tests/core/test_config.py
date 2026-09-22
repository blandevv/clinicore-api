"""Tests for src.core.config module."""

from typing import Literal

import pytest
from pydantic import SecretStr

from src.core.config import AppSettings, DatabaseSettings, Settings, get_settings


class TestAppSettings:
    """Tests for the AppSettings model."""

    def test_default_values(self) -> None:
        settings = AppSettings()
        assert settings.name == "Clinicore API"
        assert (
            settings.description
            == """
        Clinicore API is a backend service that provides a set of endpoints for 
        managing and accessing clinic-related data. It is designed to be fast, 
        secure, and scalable, making it suitable for use in healthcare applications.
    """
        )
        assert settings.version == "0.1.0"
        assert settings.env == "development"
        assert settings.debug is False

    @pytest.mark.parametrize(
        "env_value",
        ["development", "production"],
    )
    def test_valid_env_values(
        self, env_value: Literal["development", "production"]
    ) -> None:
        settings = AppSettings(env=env_value)
        assert settings.env == env_value

    def test_invalid_env_value(self) -> None:
        with pytest.raises(Exception):
            _ = AppSettings(env="invalid")  # pyright: ignore[reportArgumentType]

    def test_custom_values(self) -> None:
        settings = AppSettings(name="Custom", version="2.0.0", debug=True)
        assert settings.name == "Custom"
        assert settings.version == "2.0.0"
        assert settings.debug is True


class TestDatabaseSettings:
    """Tests for the DatabaseSettings model."""

    def test_url_construction(self) -> None:
        settings = DatabaseSettings(
            host="localhost",
            port=5432,
            name="clinicore",
            user="postgres",
            password=SecretStr("secret"),
        )
        assert (
            settings.url
            == "postgresql+asyncpg://postgres:secret@localhost:5432/clinicore"
        )

    def test_custom_port(self) -> None:
        settings = DatabaseSettings(
            host="db.host",
            port=5433,
            name="mydb",
            user="admin",
            password=SecretStr("pw"),
        )
        assert settings.url == "postgresql+asyncpg://admin:pw@db.host:5433/mydb"

    def test_password_is_secret(self) -> None:
        settings = DatabaseSettings(
            host="localhost", port=5432, name="db", user="u", password=SecretStr("p")
        )
        assert isinstance(settings.password, SecretStr)
        assert settings.password.get_secret_value() == "p"


class TestSettings:
    """Tests for the top-level Settings model."""

    def test_loads_from_env(self) -> None:
        settings = Settings()  # pyright: ignore[reportCallIssue]
        assert settings.database.host == "localhost"
        assert settings.database.name == "clinicore_test"
        assert settings.jwt_algorithm == "HS256"
        assert settings.jwt_access_token_expire_minutes == 30
        assert settings.jwt_refresh_token_expire_days == 7

    def test_jwt_secret_key_is_secret_str(self) -> None:
        settings = Settings()  # pyright: ignore[reportCallIssue]
        assert isinstance(settings.jwt_secret_key, SecretStr)

    def test_default_app_settings(self) -> None:
        settings = Settings()  # pyright: ignore[reportCallIssue]
        assert settings.app.name == "Clinicore API"


class TestGetSettings:
    """Tests for the get_settings cached function."""

    def test_returns_settings_instance(self) -> None:
        result = get_settings()
        assert isinstance(result, Settings)

    def test_returns_same_instance_on_repeated_calls(self) -> None:
        first = get_settings()
        second = get_settings()
        assert first is second

    def test_cache_clear_returns_new_instance(self) -> None:
        first = get_settings()
        get_settings.cache_clear()
        second = get_settings()
        assert first is not second
