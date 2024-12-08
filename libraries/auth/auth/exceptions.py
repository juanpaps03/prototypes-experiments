from fastapi import HTTPException
from starlette.status import HTTP_403_FORBIDDEN

http_forbidden_error = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="JWK invalid"
)
http_wrong_auth_method = HTTPException(
    status_code=HTTP_403_FORBIDDEN, detail="Wrong authentication method"
)
