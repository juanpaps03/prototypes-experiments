from auth.jwt import JwtAuthentication, JwtClaims


class ExternalJwtAuthentication(JwtAuthentication):
    def validate_token(self, token: str) -> JwtClaims:
        jwt_data = self.decode_token(token)
        jwt_claims = JwtClaims(
            client_id=jwt_data.get("clientId"),
            expiration=jwt_data.get("exp"),
        )
        return jwt_claims