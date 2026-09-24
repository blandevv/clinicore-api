"""Define the permission value object."""

from dataclasses import dataclass
from typing import override

from src.domain.enums import PermissionAction, PermissionResource


@dataclass(frozen=True)
class Permission:
    """Represent a permission defined by an action and a resource."""

    action: PermissionAction
    resource: PermissionResource

    @property
    def value(self) -> str:
        """Return the string representation of the permission."""
        return f"{self.action.value}:{self.resource.value}"

    @override
    def __str__(self) -> str:
        return self.value
