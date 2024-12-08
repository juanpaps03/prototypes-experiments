from collections.abc import Coroutine

import httpx
import structlog

from auth.internal_auth import InternalJwtAuthentication
from auth.issuers import Issuers
from fastapi import Depends

from inbound_data_gateway.example_data.models import ExampleDataPayload
from inbound_data_gateway.settings import app_settings

logger = structlog.get_logger(__name__)

# TODO: Create a client library for event sourcing example and use that instead of a localised client

async def get_httpx_client() -> Coroutine[httpx.Client]:
    async with httpx.AsyncClient() as client:
        client.base_url = str(app_settings.event_sourcing_example_url)
        client.auth = InternalJwtAuthentication(
            issuer=Issuers.EVENT_SOURCING_EXAMPLE,
            encryption_key=app_settings.internal_jwt_key
        )
        yield client


class EventSourcingExampleClient:
    _httpx_client: httpx.AsyncClient

    def __init__(self, httpx_client: httpx.AsyncClient = Depends(get_httpx_client)):
        self._httpx_client = httpx_client


    async def create_example_event(self, example_event_data: ExampleDataPayload) -> None:
        payload = example_event_data.model_dump_json()
        logger.debug(f"Sending payload to event sourcing: \n {payload}")
        response = await self._httpx_client.post(
            "create-event-data",
            data=payload
        )
        response.raise_for_status()