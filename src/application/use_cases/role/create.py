"""Define the use case for creating role entities."""

from dataclasses import dataclass, field

from src.domain.entities import RoleEntity
from src.domain.exceptions import RoleAlreadyExistsError
from src.domain.repositories import RoleRepository
from src.domain.value_objects import Permission


@dataclass(frozen=True, kw_only=True)
class CreateRoleCommand:
    """Command with the data required to create a role."""

    name: str
    description: str | None = None
    permissions: set[Permission] = field(default_factory=set)


class CreateRoleUseCase:
    """Create a new role ensuring its name is not already in use."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self.role_repository: RoleRepository = role_repository

    async def execute(self, command: CreateRoleCommand) -> RoleEntity:
        """Create the role and persist it, returning the saved role."""
        await self._ensure_role_does_not_exist(command.name)

        role = RoleEntity(
            name=command.name,
            description=command.description,
            permissions=command.permissions,
        )

        return await self.role_repository.save(role)

    async def _ensure_role_does_not_exist(self, name: str) -> None:
        """Raise an error if a role with the given name already exists."""
        if await self.role_repository.exists_by_name(name):
            raise RoleAlreadyExistsError(name)
