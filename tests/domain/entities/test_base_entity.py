from dataclasses import dataclass
from uuid import UUID

import pytest

from src.domain.entities.base_entity import BaseEntity


@dataclass(eq=False, kw_only=True)
class _OtherEntity(BaseEntity):
    """Second entity type, used only to prove equality is type-aware."""


def test_id_is_generated_automatically_when_not_provided() -> None:
    entity = BaseEntity()

    assert isinstance(entity.entity_id, UUID)


def test_two_entities_get_different_ids_by_default() -> None:
    assert BaseEntity().entity_id != BaseEntity().entity_id


@pytest.mark.parametrize(
    ("build_other", "expected"),
    [
        pytest.param(
            lambda same_id: BaseEntity(entity_id=same_id), True, id="same-type-same-id"
        ),
        pytest.param(lambda _: BaseEntity(), False, id="same-type-different-id"),
        pytest.param(
            lambda same_id: _OtherEntity(entity_id=same_id),
            False,
            id="different-type-same-id",
        ),
    ],
)
def test_equality(entity_id: UUID, build_other, expected: bool) -> None:
    entity = BaseEntity(entity_id=entity_id)
    other = build_other(entity_id)

    assert (entity == other) is expected


def test_entity_is_not_equal_to_a_non_entity_object(entity_id: UUID) -> None:
    assert BaseEntity(entity_id=entity_id) != object()


def test_entities_with_same_id_have_equal_hash(entity_id: UUID) -> None:
    assert hash(BaseEntity(entity_id=entity_id)) == hash(
        BaseEntity(entity_id=entity_id)
    )


def test_entities_with_same_id_but_different_type_have_different_hash(
    entity_id: UUID,
) -> None:
    assert hash(BaseEntity(entity_id=entity_id)) != hash(
        _OtherEntity(entity_id=entity_id)
    )


def test_entity_can_be_used_in_a_set(entity_id: UUID) -> None:
    entities = {BaseEntity(entity_id=entity_id), BaseEntity(entity_id=entity_id)}

    assert len(entities) == 1
