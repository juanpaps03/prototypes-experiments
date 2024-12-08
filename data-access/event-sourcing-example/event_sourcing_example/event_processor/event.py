import uuid
from abc import abstractmethod
from datetime import timezone, datetime
from typing import TypeVar, Generic, Any

from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.dialects.postgresql import UUID

from event_sourcing_example.event_processor.model import EventModel

T = TypeVar("T", bound=EventModel)


class Event(Generic[T]):
    id = Column(Integer(), primary_key=True)
    model_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    performed_on = Column(DateTime(timezone=True), nullable=False)
    event_name = Column(String(100), nullable=False)


    def __init__(
        self,
        event_name: str,
        model_id: uuid.UUID,
    ):
        self.event_name = event_name
        self.model_id = model_id
        self.performed_on = datetime.now(timezone.utc)


    @abstractmethod
    def trigger_event(self, model: T | None) -> T:
        ...


event_t = TypeVar("event_t", bound=Event[Any])
