"""Expose the domain repositories for convenient package-level imports."""

from .base_repository import BaseRepository
from .role_repository import RoleRepository

__all__ = ["BaseRepository", "RoleRepository"]
