from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    port: int = 3000
    build_version: str = "0.0.1"
    super_secret_key: str = "MYKey"


app_settings = AppSettings()
