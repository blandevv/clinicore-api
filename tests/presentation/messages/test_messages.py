"""Tests for the user-facing message catalog."""

from collections.abc import Iterator

import pytest

from src.domain.exceptions import DomainError
from src.presentation.messages import MessageCatalogError, get_message, registered_codes


def _iter_subclasses(cls: type[DomainError]) -> Iterator[type[DomainError]]:
    for subclass in cls.__subclasses__():
        yield subclass
        yield from _iter_subclasses(subclass)


@pytest.mark.parametrize(
    ("code", "context", "expected"),
    [
        pytest.param(
            "role_not_found",
            {"role_id": "abc"},
            "Role with ID 'abc' was not found.",
            id="role-not-found",
        ),
        pytest.param(
            "role_already_exists",
            {"role_name": "Admin"},
            "Role with name 'Admin' already exists.",
            id="role-already-exists",
        ),
        pytest.param(
            "role_already_deleted",
            {"role_id": "abc"},
            "Role with ID 'abc' has already been deleted.",
            id="role-already-deleted",
        ),
    ],
)
def test_get_message_formats_context(
    code: str, context: dict[str, str], expected: str
) -> None:
    assert get_message(code, context) == expected


def test_every_domain_error_has_a_registered_message() -> None:
    registered = registered_codes()
    for error_cls in _iter_subclasses(DomainError):
        assert error_cls.code in registered, (
            f"{error_cls.__name__} declares code {error_cls.code!r} "
            "without a registered message template"
        )


def test_get_message_raises_in_strict_env_for_unknown_code(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP__ENV", "testing")

    with pytest.raises(MessageCatalogError):
        get_message("unknown_code")


def test_get_message_raises_in_strict_env_for_missing_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP__ENV", "testing")

    with pytest.raises(MessageCatalogError):
        get_message("role_not_found", {"wrong_key": "value"})


def test_get_message_falls_back_to_code_in_production(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("APP__ENV", "production")

    assert get_message("unknown_code") == "unknown_code"
