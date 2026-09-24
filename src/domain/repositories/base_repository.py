"""Define the base repository interface for domain entities."""

from abc import ABC, abstractmethod
from uuid import UUID


class BaseRepository[T](ABC):
    """Define the contract for repositories that manage domain entities."""

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> T | None:
        """Return the entity with the specified ID, if it exists."""
        ...

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Persist the entity to the repository and return the saved entity."""
        ...
