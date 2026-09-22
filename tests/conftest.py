"""Root-level shared fixtures for the entire test suite."""

from collections.abc import Generator

import pytest


@pytest.fixture(autouse=True)
def env_settings(monkeypatch: pytest.MonkeyPatch) -> Generator[None]:
    """Set required environment variables for pydantic-settings before each tests"""
    monkeypatch.setenv("DATABASE__HOST", "localhost")
    monkeypatch.setenv("DATABASE__PORT", "5432")
    monkeypatch.setenv("DATABASE__NAME", "clinicore_test")
    monkeypatch.setenv("DATABASE__USER", "postgres")
    monkeypatch.setenv("DATABASE__PASSWORD", "postgres")
    monkeypatch.setenv("JWT_SECRET_KEY", "test-secret-key-for-unit-tests")
    yield
