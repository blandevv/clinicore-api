"""Define the HTTP endpoints for role management."""

from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends, Query, status

from src.application.use_cases.role import (
    CreateRoleCommand,
    CreateRoleUseCase,
    DeleteRoleUseCase,
    GetRoleByIdUseCase,
    ListRolesQuery,
    ListRolesUseCase,
    PatchRoleCommand,
    PatchRoleUseCase,
    UpdatePermissionsCommand,
    UpdatePermissionsUseCase,
)
from src.presentation.dependencies.role import (
    create_role_use_case,
    delete_role_use_case,
    get_role_by_id_use_case,
    list_roles_use_case,
    patch_role_use_case,
    update_permissions_use_case,
)
from src.presentation.schemas.pagination import Page
from src.presentation.schemas.role import (
    CreateRoleRequest,
    PatchRoleRequest,
    RoleResponse,
    UpdatePermissionsRequest,
)

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("", response_model=Page[RoleResponse])
async def list_roles(
    use_case: Annotated[ListRolesUseCase, Depends(list_roles_use_case)],
    name: str | None = None,
    is_active: bool | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 10,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> Page[RoleResponse]:
    """Return a paginated page of roles matching the given filters."""
    page = await use_case.execute(
        ListRolesQuery(name=name, is_active=is_active, limit=limit, offset=offset)
    )
    return Page(
        items=[RoleResponse.from_entity(role) for role in page.items],
        total=page.total,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=RoleResponse, status_code=status.HTTP_201_CREATED)
async def craate_role(
    body: CreateRoleRequest,
    use_case: Annotated[CreateRoleUseCase, Depends(create_role_use_case)],
) -> RoleResponse:
    """Create a role with the given name, description and permissions."""
    command = CreateRoleCommand(
        name=body.name,
        description=body.description,
        permissions={p.to_domain() for p in body.permissions},
    )
    role = await use_case.execute(command)
    return RoleResponse.from_entity(role)


@router.get("/{role_id}", response_model=RoleResponse)
async def get_role_by_id(
    role_id: UUID,
    use_case: Annotated[GetRoleByIdUseCase, Depends(get_role_by_id_use_case)],
) -> RoleResponse:
    """Return the role with the given identifier."""
    role = await use_case.execute(role_id)
    return RoleResponse.from_entity(role)


@router.patch("/{role_id}", response_model=RoleResponse)
async def patch_role(
    role_id: UUID,
    body: PatchRoleRequest,
    use_case: Annotated[PatchRoleUseCase, Depends(patch_role_use_case)],
) -> RoleResponse:
    """Update only the specified fields of the role."""
    command = PatchRoleCommand(
        role_id=role_id,
        name=body.name,
        description=body.description,
        is_active=body.is_active,
    )
    role = await use_case.execute(command)
    return RoleResponse.from_entity(role)


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(
    role_id: UUID, use_case: Annotated[DeleteRoleUseCase, Depends(delete_role_use_case)]
) -> None:
    """Soft-delete the role with the given identifier."""
    _ = await use_case.execute(role_id)


@router.put("/{role_id}/permissions", response_model=RoleResponse)
async def update_permissions(
    role_id: UUID,
    body: UpdatePermissionsRequest,
    use_case: Annotated[UpdatePermissionsUseCase, Depends(update_permissions_use_case)],
) -> RoleResponse:
    """Replace the full set of permissions granted to the role."""
    command = UpdatePermissionsCommand(
        role_id=role_id,
        permissions={p.to_domain() for p in body.permissions},
    )
    role = await use_case.execute(command)
    return RoleResponse.from_entity(role)
