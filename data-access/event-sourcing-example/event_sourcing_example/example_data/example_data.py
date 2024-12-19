import uuid

import structlog
from fastapi.params import Depends

from event_sourcing_example.example_data.event_models import CreateExampleDataEvent
from event_sourcing_example.example_data.event_processor import ExampleDataProcessor
from event_sourcing_example.example_data.models import ExampleData

logger = structlog.get_logger(__name__)



class ExampleDataService:
    _example_data_processor: ExampleDataProcessor

    def __init__(self, example_data_processor: ExampleDataProcessor = Depends()):
        self._example_data_processor = example_data_processor

    async def create_example_data(self, example_data: ExampleData) -> ExampleData:
        event = CreateExampleDataEvent(
            example_data_id=uuid.uuid4(),
            email=example_data.email,
        )
        self._example_data_processor.record(
            event,
            None
        )
        return example_data
