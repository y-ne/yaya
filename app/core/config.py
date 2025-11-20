from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "yaya"
    app_version: str = "0.1.0"
    debug: bool = False

    turso_database_url: str
    turso_auth_token: str
    use_embedded_replica: bool = True
    local_db_path: str = "local.db"
    sync_interval: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()
