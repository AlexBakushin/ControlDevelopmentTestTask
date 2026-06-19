from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    REDIS_URL: str
    PG_DB: str
    PG_USER: str
    PG_PASSWORD: str
    PG_HOST: str
    PG_PORT: int
    RATE_LIMIT: int = 10
    WINDOW: int = 120

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
