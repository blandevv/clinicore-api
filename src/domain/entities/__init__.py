"""Expose the domain entities for convenient package-level imports."""

from .audit_entity import AuditEntity
from .base_entity import BaseEntity
from .role_entity import RoleEntity

__all__ = ["AuditEntity", "BaseEntity", "RoleEntity"]
