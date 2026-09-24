"""Define the base entity abstraction for domain models."""

from dataclasses import dataclass, field
from typing import override
from uuid import UUID, uuid4


@dataclass(eq=False, kw_only=True)
class BaseEntity:
    """Base class for domain entities with a unique identifier."""

    entity_id: UUID = field(default_factory=uuid4)

    @override
    def __eq__(self, other: object) -> bool:
        if type(self) is not type(other):
            return NotImplemented
        return self.entity_id == other.entity_id

    @override
    def __hash__(self) -> int:
        return hash((type(self), self.entity_id))
