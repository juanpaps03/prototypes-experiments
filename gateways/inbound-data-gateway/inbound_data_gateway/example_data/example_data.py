import structlog

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

    @staticmethod
    def create_example_data(example_data: ExampleDataPayload) -> ExampleModelResponse:
        logger.debug("Working hard")
        return ExampleDataConverter(example_data).get_example_model_response()
