"""Define the use case for soft-deleting role entities."""

from uuid import UUID

from src.application.use_cases.role._shared import get_role_or_raise
from src.domain.entities import RoleEntity
from src.domain.repositories import RoleRepository


class DeleteRoleUseCase:
    """Soft-delete a role so it is no longer visible in queries."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self.role_repository: RoleRepository = role_repository

    async def execute(self, role_id: UUID) -> RoleEntity:
        """Mark the role as deleted and persist it, returning the deleted role."""
        role = await get_role_or_raise(self.role_repository, role_id)
        role.mark_deleted()
        return await self.role_repository.save(role)
