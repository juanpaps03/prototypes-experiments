from auth.exceptions import http_forbidden_error
from auth.jwt import JwtAuthentication, JwtClaims


class InternalJwtAuthentication(JwtAuthentication):

    def validate_token(self, token: str) -> JwtClaims:
        jwt_data = self.decode_token(token)
        issuer = jwt_data.pop("iss")
        if issuer != self._issuer.value:
            raise http_forbidden_error

        return JwtClaims(**jwt_data)
