import uuid

from pydantic.dataclasses import dataclass
from sqlalchemy import ForeignKey, Integer, Column, String
from sqlalchemy.orm import declarative_base

from event_sourcing_example.event_processor.event import Event
from event_sourcing_example.event_processor.model import EventModel
from event_sourcing_example.example_data.models import ExampleData, Identifier

Base: type = declarative_base()

class ExampleDataEventModel(EventModel):
    email: str

    def __init__(self, email: str):
        super().__init__()
        self.email = email


class ExampleDataEvent(Event[ExampleData], Base):
    CREATE_DATA_EVENT_NAME = "ExampleDataCreated"

    __tablename__ = "example_data_event"

    def trigger_event(self, model: ExampleDataEventModel | None) -> ExampleDataEventModel:
        raise NotImplemented


class CreateExampleDataEvent(ExampleDataEvent):

    __tablename__ = "example_data_created_event"
    __mapper_args__ = {"polymorphic_identity": ExampleDataEvent.CREATE_DATA_EVENT_NAME}

    id = Column(Integer, ForeignKey("example_data_event.id", ondelete="CASCADE"), primary_key=True)
    email = Column(String(150), nullable=True)

    def __init__(self, example_data_id: uuid.UUID, email: str):
        super().__init__(
            event_name=ExampleDataEvent.CREATE_DATA_EVENT_NAME,
            model_id=example_data_id
        )
        self.email = email


    def trigger_event(self, _: ExampleDataEventModel | None) -> ExampleDataEventModel:
        return ExampleDataEventModel(
            email=self.email
        )


