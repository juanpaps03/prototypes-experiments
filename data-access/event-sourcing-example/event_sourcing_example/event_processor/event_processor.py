from abc import abstractmethod
from typing import Generic
from uuid import UUID

from event_sourcing_example.event_processor.event import event_t
from event_sourcing_example.event_processor.model import model_t


class EventProcessor(Generic[event_t, model_t]):

    @abstractmethod
    def save_event(self, event: event_t) -> None:
        ...

    @abstractmethod
    def get_event_by_model_id(
        self, model_id: UUID
    ):
        ...

    def record(self, event: event_t, model: model_t | None) -> model_t:
        updated_model = event.trigger_event(model)
        self.save_event(event)
        return updated_model


    async def playback(self, model_id: UUID) -> model_t | None:
        model = None
        for event in self.get_event_by_model_id(model_id):
            model = event.trigger_event(model)

        return model
