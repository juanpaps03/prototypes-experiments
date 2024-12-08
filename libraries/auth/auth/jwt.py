from abc import abstractmethod

import httpx
import jwt

from typing import Optional, Any

from pydantic.alias_generators import to_camel

from auth.exceptions import http_forbidden_error
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError
from starlette.requests import Request
from pydantic import ValidationError, BaseModel, ConfigDict

from auth.issuers import Issuers

LONG_JWT_EXPIRATION = 3586374563


class JwtClaims(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        alias_generator=to_camel,
        populate_by_name=True
    )

    client_id: str | None = None
    exp: int = LONG_JWT_EXPIRATION


class JwtAuthentication(httpx.Auth):
    ENCRYPTION_ALGORITHM = "HS256"

    _issuer: Issuers
    _encryption_key: str

    def __init__(self, encryption_key: str, issuer: Issuers):
        self._issuer = issuer
        self._encryption_key = encryption_key

    def generate_token(self, jwt_claims: JwtClaims = JwtClaims()) -> str:
        jwt_payload = jwt_claims.model_dump()
        jwt_payload["iss"] = self._issuer.value
        token: str = jwt.encode(
            jwt_payload,
            self._encryption_key,
            algorithm=self.ENCRYPTION_ALGORITHM,
        )
        return token

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token, key=self._encryption_key, algorithms=[self.ENCRYPTION_ALGORITHM]
            )
        except DecodeError as error:
            raise Exception(
                "Unable to decode internal JWT malformed token"
            ) from error


    def auth_flow(self, request):
        request.headers['Authorization'] = f"Bearer {self.generate_token()}"
        yield request


    @abstractmethod
    def validate_token(self, token: str) -> JwtClaims:
        ...




class JWTBearer(HTTPBearer):
    _internal_jwt_auth: JwtAuthentication

    def __init__(
        self,
        internal_jwt_auth: JwtAuthentication,
        auto_error: bool = True,
    ):
        super().__init__(auto_error=auto_error)
        self._internal_jwt_auth = internal_jwt_auth

    async def __call__(
        self,
        request: Request
    ) -> Any:
        credentials: Optional[HTTPAuthorizationCredentials] = await super().__call__(
            request
        )
        if credentials:
            jwt_token = credentials.credentials

            try:
                jwt_data = self._internal_jwt_auth.validate_token(jwt_token)
                if not jwt_data:
                    raise http_forbidden_error
                return jwt_data
            except ValidationError as error:
                raise http_forbidden_error from error
        else:
            raise http_forbidden_error
