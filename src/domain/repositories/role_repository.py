"""Define the repository interface for managing Role entities."""

from abc import ABC, abstractmethod

from src.domain.entities import RoleEntity
from src.domain.repositories.base_repository import BaseRepository


class RoleRepository(BaseRepository[RoleEntity], ABC):
    """Define the contract for repositories that manage Role entities."""

    @abstractmethod
    async def list_roles(
        self,
        *,
        name: str | None = None,
        is_active: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[RoleEntity], int]:
        """Return a list of roles matching the specified filters and the total count."""
        ...

    @abstractmethod
    async def exists_by_name(self, name: str) -> bool:
        """Return True if a role with the specified name exists, otherwise False."""
        ...

    @abstractmethod
    async def find_by_name(self, name: str) -> RoleEntity | None:
        """Return the role with the specified name, if it exists."""
        ...
