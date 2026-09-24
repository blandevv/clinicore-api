"""Define the in-memory repository for managing Role entities."""

from typing import override
from uuid import UUID

from src.domain.entities import RoleEntity
from src.domain.repositories import RoleRepository


class InMemoryRoleRepository(RoleRepository):
    """Implement an in-memory repository for managing Role entities."""

    def __init__(self) -> None:
        """Initialize the in-memory repository with an empty dictionary."""
        self._roles: dict[UUID, RoleEntity] = {}

    @override
    async def list_roles(
        self,
        *,
        name: str | None = None,
        is_active: bool | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> tuple[list[RoleEntity], int]:
        roles = [r for r in self._roles.values() if not r.is_deleted]
        if is_active is not None:
            roles = [r for r in roles if r.is_active == is_active]
        if name is not None:
            name_lower = name.lower()
            roles = [r for r in roles if name_lower in r.name.lower()]

        return roles[offset : offset + limit], len(roles)

    @override
    async def find_by_id(self, entity_id: UUID) -> RoleEntity | None:
        role = self._roles.get(entity_id)
        return role if role and not role.is_deleted else None

    @override
    async def save(self, entity: RoleEntity) -> RoleEntity:
        self._roles[entity.entity_id] = entity
        return entity

    @override
    async def find_by_name(self, name: str) -> RoleEntity | None:
        return next(
            (r for r in self._roles.values() if r.name == name and not r.is_deleted),
            None,
        )

    @override
    async def exists_by_name(self, name: str) -> bool:
        return await self.find_by_name(name) is not None
