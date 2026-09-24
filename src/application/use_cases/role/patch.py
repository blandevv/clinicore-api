"""Define the use case for partially updating role entities."""

from dataclasses import dataclass
from uuid import UUID

from src.application.use_cases.role._shared import get_role_or_raise
from src.domain.entities import RoleEntity
from src.domain.exceptions import RoleAlreadyExistsError
from src.domain.repositories import RoleRepository


@dataclass(frozen=True, kw_only=True)
class PatchRoleCommand:
    """Optional fields to update on an existing role."""

    role_id: UUID
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class PatchRoleUseCase:
    """Partially update a role while keeping its name unique."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self._role_repository = role_repository

    async def execute(self, command: PatchRoleCommand) -> RoleEntity:
        """Apply the provided changes to the role and persist it."""
        role = await get_role_or_raise(self._role_repository, command.role_id)

        if command.name is not None:
            await self._ensure_name_is_available(command.name, role)
            role.name = command.name
        if command.description is not None:
            role.description = command.description
        if command.is_active is not None:
            if command.is_active:
                role.activate()
            else:
                role.deactivate()

        if command.name is not None or command.description is not None:
            role.mark_updated()

        return await self._role_repository.save(role)

    async def _ensure_name_is_available(
        self, name: str, current_role: RoleEntity
    ) -> None:
        """Raise an error if another role already uses the given name."""
        existing = await self._role_repository.find_by_name(name)
        if existing is not None and existing.entity_id != current_role.entity_id:
            raise RoleAlreadyExistsError(name)
