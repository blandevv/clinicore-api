import pytest

from src.domain.entities import RoleEntity
from src.domain.enums import PermissionAction, PermissionResource
from src.domain.value_objects import Permission
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@pytest.fixture
def role_repository() -> InMemoryRoleRepository:
    return InMemoryRoleRepository()


@pytest.fixture
def permission() -> Permission:
    return Permission(action=PermissionAction.READ, resource=PermissionResource.PATIENT)


@pytest.fixture
async def existing_role(role_repository: InMemoryRoleRepository) -> RoleEntity:
    return await role_repository.save(RoleEntity(name="Nurse"))
