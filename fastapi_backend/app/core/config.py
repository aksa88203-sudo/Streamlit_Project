from functools import lru_cache
from typing import Literal

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "FastAPI CRUD Service"
    APP_ENV: Literal["development", "staging", "production"] = "development"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = Field(default=False, validation_alias="APP_DEBUG")
    AUTO_CREATE_TABLES: bool = True

    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "app_user"
    MYSQL_PASSWORD: str = "app_password"
    MYSQL_DB: str = "inventory_db"
    MYSQL_CHARSET: str = "utf8mb4"

    DATABASE_URL: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def sqlalchemy_database_uri(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
            f"?charset={self.MYSQL_CHARSET}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()
