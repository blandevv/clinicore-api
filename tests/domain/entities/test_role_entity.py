from collections.abc import Callable

import pytest
from pytest_mock import MockerFixture

from src.domain.entities.role_entity import RoleEntity
from src.domain.enums import PermissionAction, PermissionResource
from src.domain.exceptions.role import RoleAlreadyDeletedError
from src.domain.value_objects import Permission


@pytest.fixture
def role() -> RoleEntity:
    return RoleEntity(name="Nurse")


@pytest.fixture
def permission() -> Permission:
    return Permission(action=PermissionAction.READ, resource=PermissionResource.PATIENT)


def test_has_permission_is_false_when_not_granted(
    role: RoleEntity, permission: Permission
) -> None:
    assert role.has_permission(permission) is False


def test_grant_adds_the_permission(role: RoleEntity, permission: Permission) -> None:
    role.grant(permission)

    assert role.has_permission(permission) is True


def test_grant_is_idempotent(role: RoleEntity, permission: Permission) -> None:
    role.grant(permission)
    role.grant(permission)

    assert role.permissions == {permission}


def test_grant_marks_the_role_as_updated(
    role: RoleEntity, permission: Permission, mocker: MockerFixture
) -> None:
    spy = mocker.spy(role, "mark_updated")

    role.grant(permission)

    spy.assert_called_once()


def test_revoke_removes_the_permission(
    role: RoleEntity, permission: Permission
) -> None:
    role.grant(permission)

    role.revoke(permission)

    assert role.has_permission(permission) is False


def test_revoke_is_a_noop_when_permission_was_not_granted(
    role: RoleEntity, permission: Permission
) -> None:
    role.revoke(permission)

    assert role.has_permission(permission) is False


def test_revoke_marks_the_role_as_updated(
    role: RoleEntity, permission: Permission, mocker: MockerFixture
) -> None:
    spy = mocker.spy(role, "mark_updated")

    role.revoke(permission)

    spy.assert_called_once()


def test_deactivate_sets_is_active_false_and_marks_updated(
    role: RoleEntity, mocker: MockerFixture
) -> None:
    spy = mocker.spy(role, "mark_updated")

    role.deactivate()

    assert role.is_active is False
    spy.assert_called_once()


def test_activate_sets_is_active_true_and_marks_updated(
    role: RoleEntity, mocker: MockerFixture
) -> None:
    role.deactivate()
    spy = mocker.spy(role, "mark_updated")

    role.activate()

    assert role.is_active is True
    spy.assert_called_once()


@pytest.mark.parametrize(
    "act",
    [
        pytest.param(lambda role, permission: role.grant(permission), id="grant"),
        pytest.param(lambda role, permission: role.revoke(permission), id="revoke"),
        pytest.param(lambda role, permission: role.activate(), id="activate"),
        pytest.param(lambda role, permission: role.deactivate(), id="deactivate"),
    ],
)
def test_raises_when_role_is_deleted(
    role: RoleEntity,
    permission: Permission,
    act: Callable[[RoleEntity, Permission], None],
) -> None:
    role.mark_deleted()

    with pytest.raises(RoleAlreadyDeletedError):
        act(role, permission)


def test_deleted_role_error_carries_role_id(
    role: RoleEntity, permission: Permission
) -> None:
    role.mark_deleted()

    with pytest.raises(RoleAlreadyDeletedError) as exc_info:
        role.grant(permission)

    assert exc_info.value.context == {"role_id": str(role.entity_id)}
