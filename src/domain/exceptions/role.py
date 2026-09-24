"""Define exceptions related to role management."""

from uuid import UUID

from src.domain.exceptions.domain import DomainError


class RoleNotFoundError(DomainError):
    """Raised when a requested role does not exist."""

    code: str = "role_not_found"

    def __init__(self, role_id: UUID) -> None:
        """Initialize the error with the missing role's ID."""
        super().__init__(context={"role_id": str(role_id)})


class RoleAlreadyExistsError(DomainError):
    """Raised when attempting to create a role that already exists."""

    code: str = "role_already_exists"

    def __init__(self, role_name: str) -> None:
        """Initialize the error with the existing role's name."""
        super().__init__(context={"role_name": role_name})


class RoleAlreadyDeletedError(DomainError):
    """Raised when attempting to delete a role that is already deleted."""

    code: str = "role_already_deleted"

    def __init__(self, role_id: UUID) -> None:
        """Initialize the error with the deleted role's ID."""
        super().__init__(context={"role_id": str(role_id)})
