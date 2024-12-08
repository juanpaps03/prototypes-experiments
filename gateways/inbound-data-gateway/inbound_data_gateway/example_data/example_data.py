import structlog
from fastapi import Depends

from inbound_data_gateway.clients.event_sourcing_example_client import EventSourcingExampleClient
from inbound_data_gateway.example_data.models import ExampleModelResponse, ExampleDataPayload

logger = structlog.get_logger(__name__)


class ExampleDataConverter:
    _example_data: ExampleDataPayload

    def __init__(self, example_data: ExampleDataPayload):
        self._example_data = example_data

    def get_example_model_response(self) -> ExampleModelResponse:
        return ExampleModelResponse(
            email=self._example_data.email
        )



class ExampleDataService:
    _event_sourcing_example_client: EventSourcingExampleClient

    def __init__(self, event_sourcing_example_client: EventSourcingExampleClient = Depends()):
        self._event_sourcing_example_client = event_sourcing_example_client


    async def create_example_data(self, example_data: ExampleDataPayload) -> ExampleModelResponse:
        await self._event_sourcing_example_client.create_example_event(example_data)

        return ExampleDataConverter(example_data).get_example_model_response()
