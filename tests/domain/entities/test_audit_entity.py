from collections.abc import Callable
from datetime import UTC, datetime
from typing import override
from uuid import uuid4

import pytest

from src.domain.entities import audit_entity as audit_module
from src.domain.entities.audit_entity import AuditEntity


@pytest.fixture
def set_now(monkeypatch: pytest.MonkeyPatch) -> Callable[[datetime], None]:
    def _set(value: datetime) -> None:
        class _FrozenDatetime(datetime):
            @classmethod
            @override
            def now(cls, tz: object = None) -> datetime:
                return value

        monkeypatch.setattr(audit_module, "datetime", _FrozenDatetime)

    return _set


def test_created_at_and_updated_at_default_to_creation_time(
    set_now: Callable[[datetime], None],
) -> None:
    now = datetime(2026, 1, 1, tzinfo=UTC)
    set_now(now)

    entity = AuditEntity()

    assert entity.created_at == now
    assert entity.updated_at == now


def test_is_not_deleted_by_default() -> None:
    entity = AuditEntity()

    assert entity.is_deleted is False
    assert entity.deleted_at is None
    assert entity.deleted_by is None


def test_mark_deleted_sets_deleted_at_and_deleted_by(
    set_now: Callable[[datetime], None],
) -> None:
    entity = AuditEntity()
    by = uuid4()
    now = datetime(2026, 1, 2, tzinfo=UTC)
    set_now(now)

    entity.mark_deleted(by=by)

    assert entity.is_deleted is True
    assert entity.deleted_at == now
    assert entity.deleted_by == by


def test_mark_updated_refreshes_updated_at_and_sets_updated_by(
    set_now: Callable[[datetime], None],
) -> None:
    entity = AuditEntity()
    by = uuid4()
    now = datetime(2026, 1, 2, tzinfo=UTC)
    set_now(now)

    entity.mark_updated(by=by)

    assert entity.updated_at == now
    assert entity.updated_by == by


def test_restore_clears_deletion_and_refreshes_updated_at(
    set_now: Callable[[datetime], None],
) -> None:
    entity = AuditEntity()
    entity.mark_deleted(by=uuid4())
    now = datetime(2026, 1, 3, tzinfo=UTC)
    set_now(now)

    entity.restore()

    assert entity.is_deleted is False
    assert entity.deleted_at is None
    assert entity.deleted_by is None
    assert entity.updated_at == now
    assert entity.updated_by is None
