import pytest

from src.application.use_cases.role.create import CreateRoleCommand, CreateRoleUseCase
from src.domain.exceptions import RoleAlreadyExistsError
from src.domain.value_objects import Permission
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@pytest.fixture
def use_case(role_repository: InMemoryRoleRepository) -> CreateRoleUseCase:
    return CreateRoleUseCase(role_repository)


async def test_creates_a_role_with_the_given_name(use_case: CreateRoleUseCase) -> None:
    role = await use_case.execute(CreateRoleCommand(name="Nurse"))

    assert role.name == "Nurse"


async def test_creates_a_role_with_no_permissions_by_default(
    use_case: CreateRoleUseCase,
) -> None:
    role = await use_case.execute(CreateRoleCommand(name="Nurse"))

    assert role.permissions == set()


async def test_creates_a_role_with_the_given_permissions(
    use_case: CreateRoleUseCase, permission: Permission
) -> None:
    role = await use_case.execute(
        CreateRoleCommand(name="Nurse", permissions={permission})
    )

    assert role.permissions == {permission}


async def test_persists_the_role_in_the_repository(
    use_case: CreateRoleUseCase, role_repository: InMemoryRoleRepository
) -> None:
    role = await use_case.execute(CreateRoleCommand(name="Nurse"))

    assert await role_repository.find_by_id(role.entity_id) == role


async def test_raises_when_name_is_already_taken(use_case: CreateRoleUseCase) -> None:
    _ = await use_case.execute(CreateRoleCommand(name="Nurse"))

    with pytest.raises(RoleAlreadyExistsError):
        _ = await use_case.execute(CreateRoleCommand(name="Nurse"))
