from pydantic_core._pydantic_core import Url
from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    port: int = 3000
    build_version: str = "0.0.1"
    super_secret_key: str = "MYKey"
    internal_jwt_key: str = "InternalKey"
    event_sourcing_example_url: Url = "http://localhost:3001"

app_settings = AppSettings()
