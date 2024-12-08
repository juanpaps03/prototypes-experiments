from fastapi import APIRouter, Depends
import structlog

from event_sourcing_example.example_data.example_data import ExampleDataService
from event_sourcing_example.example_data.models import ExampleData

event_sourcing_example_route = APIRouter()

logger = structlog.get_logger(__name__)


@event_sourcing_example_route.post(
    "/create-event-data",
    status_code=201,
    response_model=ExampleData,
)
async def add_example_data(
    example_data: ExampleData,
    example_service: ExampleDataService = Depends(),
) -> ExampleData:
    logger.debug("Processing request to add data into the system")
    return await example_service.create_example_data(example_data)



