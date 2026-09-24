import pytest

from src.application.use_cases.role.patch import PatchRoleCommand, PatchRoleUseCase
from src.domain.entities import RoleEntity
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@pytest.fixture
def use_case(role_repository: InMemoryRoleRepository) -> PatchRoleUseCase:
    return PatchRoleUseCase(role_repository)


async def test_patches_is_active(
    use_case: PatchRoleUseCase,
    existing_role: RoleEntity,
    role_repository: InMemoryRoleRepository,
) -> None:
    role = await use_case.execute(
        PatchRoleCommand(role_id=existing_role.entity_id, is_active=False)
    )

    assert role.is_active is False
    persisted = await role_repository.find_by_id(existing_role.entity_id)
    assert persisted is not None
    assert persisted.is_active is False


async def test_reactivates_a_deactivated_role(
    use_case: PatchRoleUseCase, existing_role: RoleEntity
) -> None:
    existing_role.deactivate()
    _ = await use_case.execute(
        PatchRoleCommand(role_id=existing_role.entity_id, is_active=True)
    )
    assert existing_role.is_active is True


async def test_patches_name(
    use_case: PatchRoleUseCase, existing_role: RoleEntity
) -> None:
    role = await use_case.execute(
        PatchRoleCommand(role_id=existing_role.entity_id, name="Admin")
    )
    assert role.name == "Admin"


async def test_patches_description(
    use_case: PatchRoleUseCase, existing_role: RoleEntity
) -> None:
    role = await use_case.execute(
        PatchRoleCommand(role_id=existing_role.entity_id, description="New description")
    )
    assert role.description == "New description"


async def test_none_fields_are_ignored(
    use_case: PatchRoleUseCase,
    existing_role: RoleEntity,
) -> None:
    role = await use_case.execute(PatchRoleCommand(role_id=existing_role.entity_id))
    assert role.is_active is True
    assert role.name == "Nurse"
    assert role.description is None
