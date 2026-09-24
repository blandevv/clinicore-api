"""Define generic pagination response schemas."""

from pydantic import BaseModel


class Page[T](BaseModel):
    """Generic page of items with pagination metadata."""

    items: list[T]
    total: int
    limit: int
    offset: int
