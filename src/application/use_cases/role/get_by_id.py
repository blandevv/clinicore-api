"""Define the use case for retrieving a role by its identifier."""

from uuid import UUID

from src.application.use_cases.role._shared import get_role_or_raise
from src.domain.entities import RoleEntity
from src.domain.repositories import RoleRepository


class GetRoleByIdUseCase:
    """Retrieve a role by ID, raising an error if it does not exist."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self.role_repository: RoleRepository = role_repository

    async def execute(self, role_id: UUID) -> RoleEntity:
        """Return the role with the given ID or raise a not-found error."""
        return await get_role_or_raise(self.role_repository, role_id)
