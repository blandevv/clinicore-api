"""Expose the role use cases for convenient package-level imports."""

from .create import CreateRoleCommand, CreateRoleUseCase
from .delete import DeleteRoleUseCase
from .get_by_id import GetRoleByIdUseCase
from .list import ListRolesQuery, ListRolesUseCase
from .patch import PatchRoleCommand, PatchRoleUseCase
from .update_permissions import UpdatePermissionsCommand, UpdatePermissionsUseCase

__all__ = [
    "CreateRoleCommand",
    "CreateRoleUseCase",
    "DeleteRoleUseCase",
    "GetRoleByIdUseCase",
    "ListRolesQuery",
    "ListRolesUseCase",
    "PatchRoleCommand",
    "PatchRoleUseCase",
    "UpdatePermissionsCommand",
    "UpdatePermissionsUseCase",
]
