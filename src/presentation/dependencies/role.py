"""Define FastAPI dependencies that provide role use cases."""

from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from src.application.use_cases.role import (
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetRoleByIdUseCase,
    ListRolesUseCase,
    PatchRoleUseCase,
    UpdatePermissionsUseCase,
)
from src.domain.repositories import RoleRepository
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@lru_cache
def get_role_repository() -> RoleRepository:
    """Return a cached shared in-memory role repository instance."""
    return InMemoryRoleRepository()


RoleRepositoryDep = Annotated[RoleRepository, Depends(get_role_repository)]


def get_role_by_id_use_case(role_repository: RoleRepositoryDep) -> GetRoleByIdUseCase:
    """Return a GetRoleByIdUseCase wired to the given repository."""
    return GetRoleByIdUseCase(role_repository)


def list_roles_use_case(role_repository: RoleRepositoryDep) -> ListRolesUseCase:
    """Return a ListRolesUseCase wired to the given repository."""
    return ListRolesUseCase(role_repository)


def create_role_use_case(role_repository: RoleRepositoryDep) -> CreateRoleUseCase:
    """Return a CreateRoleUseCase wired to the given repository."""
    return CreateRoleUseCase(role_repository)


def patch_role_use_case(role_repository: RoleRepositoryDep) -> PatchRoleUseCase:
    """Return a PatchRoleUseCase wired to the given repository."""
    return PatchRoleUseCase(role_repository)


def delete_role_use_case(role_repository: RoleRepositoryDep) -> DeleteRoleUseCase:
    """Return a DeleteRoleUseCase wired to the given repository."""
    return DeleteRoleUseCase(role_repository)


def update_permissions_use_case(
    role_repository: RoleRepositoryDep,
) -> UpdatePermissionsUseCase:
    """Return an UpdatePermissionsUseCase wired to the given repository."""
    return UpdatePermissionsUseCase(role_repository)
