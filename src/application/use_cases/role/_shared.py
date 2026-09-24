from uuid import UUID

from src.domain.entities import RoleEntity
from src.domain.exceptions import RoleNotFoundError
from src.domain.repositories import RoleRepository


async def get_role_or_raise(
    role_repository: RoleRepository, role_id: UUID
) -> RoleEntity:
    """Retrieve a role by its ID or raise a RoleNotFoundError if not found."""
    role = await role_repository.find_by_id(role_id)
    if role is None:
        raise RoleNotFoundError(role_id)
    return role
