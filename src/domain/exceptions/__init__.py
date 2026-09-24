"""Expose domain exceptions for package-level imports."""

from .domain import DomainError
from .role import (
    RoleAlreadyDeletedError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)

__all__ = [
    "DomainError",
    "RoleAlreadyDeletedError",
    "RoleAlreadyExistsError",
    "RoleNotFoundError",
]
