"""Define HTTP exception handlers that translate domain errors."""

from typing import cast

from fastapi import Request, status
from fastapi.responses import JSONResponse

from src.domain.exceptions import DomainError
from src.presentation.messages import get_message

DOMAIN_ERROR_STATUS: dict[str, int] = {
    "role_not_found": status.HTTP_404_NOT_FOUND,
    "role_already_exists": status.HTTP_409_CONFLICT,
    "role_already_deleted": status.HTTP_409_CONFLICT,
}


async def domain_error_handler(_: Request, exc: Exception) -> JSONResponse:
    """Return the domain error with its mapped HTTP status code."""
    domain_exc = cast(DomainError, exc)
    return JSONResponse(
        status_code=DOMAIN_ERROR_STATUS.get(
            domain_exc.code, status.HTTP_422_UNPROCESSABLE_CONTENT
        ),
        content={
            "code": domain_exc.code,
            "context": domain_exc.context,
            "message": get_message(domain_exc.code, domain_exc.context),
        },
    )
