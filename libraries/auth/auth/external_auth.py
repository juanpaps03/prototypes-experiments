from auth.issuers import Issuers
from auth.jwt import JwtAuthentication, JwtClaims

from auth.exceptions import http_forbidden_error


class ExternalJwtAuthentication(JwtAuthentication):

    def __init__(self, encryption_key: str, issuer: Issuers = Issuers.EXTERNAL):
        super().__init__(encryption_key, issuer)

    def validate_token(self, token: str) -> JwtClaims:
        jwt_data = self.decode_token(token)
        issuer = jwt_data.pop("iss")

        if issuer != self._issuer.value:
            raise http_forbidden_error

        if "clientId" not in jwt_data:
            raise http_forbidden_error

        return JwtClaims(**jwt_data)