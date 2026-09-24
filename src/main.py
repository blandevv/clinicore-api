"""Application entry point for the Clinicore API."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from src.core.config import settings
from src.domain.exceptions import DomainError
from src.presentation.exception_handlers import domain_error_handler
from src.presentation.routers import role_router

app = FastAPI(
    title=settings.app.name,
    description=settings.app.description,
    version=settings.app.version,
    debug=settings.app.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.add_exception_handler(DomainError, domain_error_handler)

app.include_router(role_router)


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    """Redirect the API root to the interactive documentation."""
    return RedirectResponse(url="/docs")


@app.get("/health")
def health() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "ok"}
