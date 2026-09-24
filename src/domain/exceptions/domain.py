"""Define the base exception class for domain-level errors."""


class DomainError(Exception):
    """Base exception for errors raised by domain logic."""

    code: str = "domain_error"

    def __init__(self, context: dict[str, object] | None = None) -> None:
        """Initialize a domain error with structured context values."""
        self.context: dict[str, object] = context or {}
        super().__init__(self.code, self.context)
