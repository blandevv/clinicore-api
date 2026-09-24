"""Define the use case for replacing the permissions of a role."""

from dataclasses import dataclass
from uuid import UUID

from src.application.use_cases.role._shared import get_role_or_raise
from src.domain.entities import RoleEntity
from src.domain.repositories import RoleRepository
from src.domain.value_objects import Permission


@dataclass(frozen=True, kw_only=True)
class UpdatePermissionsCommand:
    """Role identifier and the full set of permissions to assign."""

    role_id: UUID
    permissions: set[Permission]


class UpdatePermissionsUseCase:
    """Replace the permissions granted to a role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self._role_repository = role_repository

    async def execute(self, command: UpdatePermissionsCommand) -> RoleEntity:
        """Set the role permissions and persist the updated role."""
        role = await get_role_or_raise(self._role_repository, command.role_id)
        role.permissions = command.permissions
        role.mark_updated()
        return await self._role_repository.save(role)
