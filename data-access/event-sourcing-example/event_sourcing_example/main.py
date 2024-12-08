from typing import Any

import uvicorn
from fastapi import FastAPI, Depends, APIRouter

from event_sourcing_example.api.event_sourcing_example import event_sourcing_example_route
from event_sourcing_example.settings import app_settings
from auth.internal_auth import InternalJwtAuthentication
from auth.issuers import Issuers
from auth.jwt import JWTBearer

app = FastAPI()

security = JWTBearer(internal_jwt_auth=InternalJwtAuthentication(
    issuer=Issuers.EVENT_SOURCING_EXAMPLE,
    encryption_key=app_settings.super_secret_key
))

@app.get("/healthcheck")
async def healthcheck() -> Any:
    return {"status": "ok", "version": app_settings.build_version}


api_router = APIRouter()

api_router.include_router(event_sourcing_example_route, prefix="")



pipeline = [Depends(security)]

app.include_router(api_router, dependencies=pipeline)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=app_settings.port)