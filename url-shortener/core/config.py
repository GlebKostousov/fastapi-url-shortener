"""Module for storage config data"""

import logging
from pathlib import Path
from typing import Literal, Self

from pydantic import BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level_name: Literal[
        "DEBUG",
        "INFO",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ] = "INFO"
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"

    @property
    def log_level(self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]


class RedisSetNames(BaseModel):
    tokens: str = "tokens"


class RedisHashNames(BaseModel):
    short_url: str = "short-urls"


class RedisCollectionNames(BaseModel):
    set_name: RedisSetNames = RedisSetNames()
    hash_names: RedisHashNames = RedisHashNames()


class RedisDbNumbers(BaseModel):
    tokens: int = 1
    users: int = 2
    short_urls: int = 3
    default: int = 0

    @model_validator(mode="after")
    def validate_dbs_numbers_unique(self) -> Self:
        model_dict = self.model_dump(mode="python")
        unique_values = set(model_dict.values())
        if len(unique_values) == len(model_dict):
            return self

        msg = "Database number shut be unique!"
        raise ValueError(msg)


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDbNumbers = RedisDbNumbers()
    namespace: RedisCollectionNames = RedisCollectionNames()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,  # Если True, то учитываем регистр
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        env_nested_delimiter="__",
        env_prefix="URL_SHORTENER__",
    )

    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
