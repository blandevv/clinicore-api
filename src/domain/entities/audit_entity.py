"""Define the audit entity for tracking creation, update, and deletion."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID

from src.domain.entities.base_entity import BaseEntity


@dataclass
class AuditEntity(BaseEntity):
    """Base entity with audit information and soft-delete support."""

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    deleted_at: datetime | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None
    deleted_by: UUID | None = None

    @property
    def is_deleted(self) -> bool:
        """Return whether the entity has been soft-deleted."""
        return self.deleted_at is not None

    def mark_updated(self, by: UUID | None = None) -> None:
        """Mark the entity as updated by the specified user."""
        self.updated_at = datetime.now(UTC)
        self.updated_by = by

    def mark_deleted(self, by: UUID | None = None) -> None:
        """Mark the entity as deleted by the specified user."""
        self.deleted_at = datetime.now(UTC)
        self.deleted_by = by

    def restore(self, by: UUID | None = None) -> None:
        """Restore the entity from a soft-deleted state."""
        self.deleted_at = None
        self.deleted_by = None
        self.mark_updated(by=by)
