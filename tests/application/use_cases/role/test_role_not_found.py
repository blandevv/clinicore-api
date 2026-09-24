from collections.abc import Awaitable, Callable
from uuid import uuid4

import pytest

from src.application.use_cases.role.delete import DeleteRoleUseCase
from src.application.use_cases.role.patch import (
    PatchRoleCommand,
    PatchRoleUseCase,
)
from src.application.use_cases.role.update_permissions import (
    UpdatePermissionsCommand,
    UpdatePermissionsUseCase,
)
from src.domain.exceptions import RoleNotFoundError
from src.domain.value_objects import Permission
from src.infrastructure.repositories.in_memory.role_repository import (
    InMemoryRoleRepository,
)


@pytest.mark.parametrize(
    "execute",
    [
        pytest.param(
            lambda repo, permission: DeleteRoleUseCase(repo).execute(uuid4()),
            id="delete-role",
        ),
        pytest.param(
            lambda repo, permission: PatchRoleUseCase(repo).execute(
                PatchRoleCommand(role_id=uuid4())
            ),
            id="patch-role",
        ),
        pytest.param(
            lambda repo, permission: UpdatePermissionsUseCase(repo).execute(
                UpdatePermissionsCommand(role_id=uuid4(), permissions={permission})
            ),
            id="update-permissions",
        ),
    ],
)
async def test_raises_when_role_does_not_exist(
    execute: Callable[[InMemoryRoleRepository, Permission], Awaitable[object]],
    role_repository: InMemoryRoleRepository,
    permission: Permission,
) -> None:
    with pytest.raises(RoleNotFoundError):
        _ = await execute(role_repository, permission)
