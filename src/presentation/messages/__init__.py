"""Resolve user-facing messages for domain error codes."""

import importlib
import os
from pathlib import Path

_MESSAGES: dict[str, str] = {}


def _load_catalogs() -> dict[str, str]:
    """Collect MESSAGES from every module in this package, except __init__."""
    catalogs: dict[str, str] = {}
    for module_path in Path(__file__).parent.glob("*.py"):
        if module_path.name == "__init__.py":
            continue
        module = importlib.import_module(f"{__name__}.{module_path.stem}")
        messages = getattr(module, "MESSAGES", None)
        if isinstance(messages, dict):
            catalogs.update(messages)
    return catalogs


_MESSAGES = _load_catalogs()


class MessageCatalogError(RuntimeError):
    """Raised when a message cannot be resolved in strict environments."""


def _is_strict() -> bool:
    return os.environ.get("APP__ENV", "production") in {"testing", "development"}


def _fallback(code: str) -> str:
    if _is_strict():
        raise MessageCatalogError(f"no message registered for code {code!r}")
    return code


def get_message(code: str, context: dict[str, object] | None = None) -> str:
    """Return the user-facing message for the code, applying its context."""
    template = _MESSAGES.get(code)
    if template is None:
        return _fallback(code)
    try:
        return template.format(**(context or {}))
    except KeyError as exc:
        if not _is_strict():
            return code
        raise MessageCatalogError(
            f"context key {exc.args[0]!r} is missing for message code {code!r}"
        ) from exc


def registered_codes() -> frozenset[str]:
    """Return the codes that currently have a registered message template."""
    return frozenset(_MESSAGES)
