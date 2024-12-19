from uuid import UUID

from fastapi import Depends

from event_sourcing_example.event_processor.event_processor import EventProcessor
from event_sourcing_example.example_data.event_models import ExampleDataEvent, ExampleDataEventModel
from event_sourcing_example.example_data.repository import ExampleDataRepository


class ExampleDataProcessor(EventProcessor[ExampleDataEvent, ExampleDataEventModel]):
    _example_data_repository: ExampleDataRepository

    def __init__(self, example_data_repository: ExampleDataRepository = Depends()):
        self._example_data_repository = example_data_repository

    def save_event(self, model: ExampleDataEvent) -> None:
        self._example_data_repository.add_event(model)

    async def get_event_by_model_id(self, model_id: UUID):
        pass
