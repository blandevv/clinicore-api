"""Define the use case for listing role entities with filters."""

from dataclasses import dataclass

from src.domain.entities import RoleEntity
from src.domain.repositories import RoleRepository


@dataclass(frozen=True, kw_only=True)
class ListRolesQuery:
    """Query parameters for filtering and paginating roles."""

    name: str | None = None
    is_active: bool | None = None
    limit: int = 10
    offset: int = 0


@dataclass(frozen=True, kw_only=True)
class RolePage:
    """A page of roles with the total number of matching roles."""

    items: list[RoleEntity]
    total: int


class ListRolesUseCase:
    """List roles matching the query filters with pagination."""

    def __init__(self, role_repository: RoleRepository) -> None:
        """Initialize the use case with a role repository."""
        self.role_repository: RoleRepository = role_repository

    async def execute(self, query: ListRolesQuery) -> RolePage:
        """Return the page of roles matching the given query filters."""
        roles, total = await self.role_repository.list_roles(
            name=query.name,
            is_active=query.is_active,
            limit=query.limit,
            offset=query.offset,
        )
        return RolePage(items=roles, total=total)
