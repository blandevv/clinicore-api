"""Shared fixtures for core module tests."""

from collections.abc import Generator

import pytest


@pytest.fixture(autouse=True)
def _clear_settings_cache() -> Generator[None]:
    """Clear the lru_cache on get_settings before each tests."""
    from src.core.config import get_settings

    get_settings.cache_clear()
    yield
    get_settings.cache_clear()
