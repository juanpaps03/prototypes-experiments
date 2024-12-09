from typing import Any

import uvicorn
from fastapi import FastAPI, Depends, APIRouter

from inbound_data_gateway.api.example_data import example_data_router
from inbound_data_gateway.settings import app_settings
from auth.external_auth import ExternalJwtAuthentication
from auth.issuers import Issuers
from auth.jwt import JWTBearer

app = FastAPI()
security = JWTBearer(
    internal_jwt_auth=ExternalJwtAuthentication(
        issuer=Issuers.EXTERNAL,
        encryption_key=app_settings.super_secret_key
    )
)

@app.get("/healthcheck")
async def healthcheck() -> Any:
    return {"status": "ok", "version": app_settings.build_version}


api_router = APIRouter()

api_router.include_router(example_data_router, prefix="/example-data")


pipeline = [Depends(security)]

app.include_router(api_router, dependencies=pipeline)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=app_settings.port)