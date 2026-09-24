import pytest

from src.application.use_cases.role.delete import DeleteRoleUseCase
from src.domain.entities import RoleEntity
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@pytest.fixture
def use_case(role_repository: InMemoryRoleRepository) -> DeleteRoleUseCase:
    return DeleteRoleUseCase(role_repository)


async def test_soft_deletes_the_role(
    use_case: DeleteRoleUseCase,
    existing_role: RoleEntity,
    role_repository: InMemoryRoleRepository,
) -> None:
    role = await use_case.execute(existing_role.entity_id)

    assert role.is_deleted is True
    assert role.is_active is True

    persisted = await role_repository.find_by_id(existing_role.entity_id)
    assert persisted is None
