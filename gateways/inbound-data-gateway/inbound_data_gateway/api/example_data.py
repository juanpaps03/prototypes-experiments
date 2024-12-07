from fastapi import APIRouter, Depends
import structlog

from inbound_data_gateway.example_data.example_data import ExampleDataService
from inbound_data_gateway.example_data.models import ExampleDataPayload, ExampleModelResponse

example_data_router = APIRouter()

logger = structlog.get_logger(__name__)


@example_data_router.post(
    "",
    status_code=201,
    response_model=ExampleModelResponse,
)
async def add_example_data(
    example_data: ExampleDataPayload,
    example_service: ExampleDataService = Depends(),
) -> ExampleModelResponse:
    logger.debug("Processing request to add data into the system")
    return await example_service.create_example_data(example_data)



