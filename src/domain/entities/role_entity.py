"""Define the role entity for managing permissions and activation state."""

from dataclasses import dataclass, field

from src.domain.entities.audit_entity import AuditEntity
from src.domain.exceptions import RoleAlreadyDeletedError
from src.domain.value_objects import Permission


@dataclass(eq=False, kw_only=True)
class RoleEntity(AuditEntity):
    """Domain entity representing a role with permissions and activation state."""

    name: str
    description: str | None = None
    permissions: set[Permission] = field(default_factory=set)
    is_active: bool = True

    def has_permission(self, permission: Permission) -> bool:
        """Return whether the role has the specified permission."""
        return permission in self.permissions

    def grant(self, permission: Permission) -> None:
        """Grant a permission to the role."""
        self._ensure_not_deleted()
        self.permissions.add(permission)
        self.mark_updated()

    def revoke(self, permission: Permission) -> None:
        """Revoke a permission from the role."""
        self._ensure_not_deleted()
        self.permissions.discard(permission)
        self.mark_updated()

    def activate(self) -> None:
        """Activate the role."""
        self._ensure_not_deleted()
        if not self.is_active:
            self.is_active = True
            self.mark_updated()

    def deactivate(self) -> None:
        """Deactivate the role."""
        self._ensure_not_deleted()
        if self.is_active:
            self.is_active = False
            self.mark_updated()

    def _ensure_not_deleted(self) -> None:
        """Raise an error if the role has been deleted."""
        if self.is_deleted:
            raise RoleAlreadyDeletedError(self.entity_id)
