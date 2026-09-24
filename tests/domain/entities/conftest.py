from uuid import UUID, uuid4

import pytest


@pytest.fixture
def entity_id() -> UUID:
    """Fixture to generate a unique entity ID."""
    return uuid4()
