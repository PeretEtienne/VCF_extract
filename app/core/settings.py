from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ELASTICSEARCH_URL: str = Field(default=...)
    ELASTICSEARCH_USER: str = Field(default=...)
    ELASTICSEARCH_PASSWORD: str = Field(default=...)

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
