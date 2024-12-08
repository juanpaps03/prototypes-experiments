import uuid
from dataclasses import dataclass
from typing import TypeVar


class EventModel:
    id: uuid.UUID

    def __init__(self, entity_id: uuid.UUID | None = None) -> None:
        self.id = entity_id or uuid.uuid4()


model_t = TypeVar("model_t", bound=EventModel)