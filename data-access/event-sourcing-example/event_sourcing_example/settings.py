from pydantic_settings import BaseSettings


class AppSettings(BaseSettings):
    port: int = 3001
    build_version: str = "0.0.1"
    super_secret_key: str = "InternalKey"
    db_url: str = "postgresql://user:password@localhost/event_sourcing_local"


app_settings = AppSettings()
