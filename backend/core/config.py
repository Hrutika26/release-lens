from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "Release Lens"
    database_url: str
    db_pool_min_size: int
    db_pool_max_size: int

settings = Settings()
