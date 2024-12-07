from dataclasses import dataclass
from typing import Optional, Any

import jwt
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import DecodeError
from starlette.requests import Request
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import ValidationError


LONG_JWT_EXPIRATION = 3586374563

http_forbidden_error = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
)
http_wrong_auth_method = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
)


@dataclass(frozen=True)
class JwtClaims:
    identifier: str = None
    client_id: str = None
    expiration: int = LONG_JWT_EXPIRATION


class JwtAuthentication:
    ENCRYPTION_ALGORITHM = "HS256"

    _issuer: str
    _encryption_key: str

    def __init__(self, encryption_key: str, issuer: str):
        self._issuer = issuer
        self._encryption_key = encryption_key

    def generate_token(self, jwt_claims: JwtClaims = JwtClaims()) -> str:
        claims = {
            "clientId": jwt_claims.client_id,
            "iss": self._issuer,
            "exp": jwt_claims.expiration,
        }
        token: str = jwt.encode(
            claims,
            self._encryption_key,
            algorithm=self.ENCRYPTION_ALGORITHM,
        )
        return token

    def decode_token(self, token: str) -> Any:
        try:
            return jwt.decode(
                token, key=self._encryption_key, algorithms=[self.ENCRYPTION_ALGORITHM]
            )
        except DecodeError as error:
            raise Exception(
                "Unable to decode internal JWT malformed token"
            ) from error

    def validate_token(self, token: str) -> JwtClaims:
        raise NotImplementedError




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
    ) -> JwtClaims:
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
