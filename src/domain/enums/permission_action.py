"""Define the actions available for permission management."""

from enum import StrEnum


class PermissionAction(StrEnum):
    """Represent an operation that can be granted or revoked as a permission."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    ACTIVATE = "activate"
    DEACTIVATE = "deactivate"
    ASSIGN = "assign"
    UNASSIGN = "unassign"
    CANCEL = "cancel"
    RESCHEDULE = "reschedule"
    CONFIRM = "confirm"
