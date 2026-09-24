"""Define request and response schemas for the role API."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from src.domain.entities import RoleEntity
from src.domain.enums import PermissionAction, PermissionResource
from src.domain.value_objects import Permission


class PermissionSchema(BaseModel):
    """Represent a permission as an action/resource pair."""

    action: PermissionAction
    resource: PermissionResource

    def to_domain(self) -> Permission:
        """Convert the schema into the domain Permission value object."""
        return Permission(action=self.action, resource=self.resource)

    @classmethod
    def from_domain(cls, permission: Permission) -> PermissionSchema:
        """Build a schema from a domain Permission value object."""
        return cls(action=permission.action, resource=permission.resource)


class CreateRoleRequest(BaseModel):
    """Request body for creating a role."""

    name: str
    description: str | None = None
    permissions: list[PermissionSchema] = Field(default_factory=list)


class PatchRoleRequest(BaseModel):
    """Request body for partially updating a role."""

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdatePermissionsRequest(BaseModel):
    """Request body for replacing the permissions of a role."""

    permissions: list[PermissionSchema] = Field(default_factory=list)


class RoleResponse(BaseModel):
    """Response payload representing a role."""

    id: UUID
    name: str
    description: str | None = None
    is_active: bool
    permissions: list[PermissionSchema]
    created_at: datetime
    updated_at: datetime
    deleted_at: datetime | None = None
    created_by: UUID | None = None
    updated_by: UUID | None = None
    deleted_by: UUID | None = None

    @classmethod
    def from_entity(cls, role: RoleEntity) -> RoleResponse:
        """Build a response schema from a domain RoleEntity."""
        return cls(
            id=role.entity_id,
            name=role.name,
            description=role.description,
            is_active=role.is_active,
            permissions=[PermissionSchema.from_domain(p) for p in role.permissions],
            created_at=role.created_at,
            updated_at=role.updated_at,
            deleted_at=role.deleted_at,
            created_by=role.created_by,
            updated_by=role.updated_by,
            deleted_by=role.deleted_by,
        )
