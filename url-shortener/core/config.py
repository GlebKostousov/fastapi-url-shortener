"""Module for storage config data"""

import logging
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

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


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()
    db: RedisDbNumbers = RedisDbNumbers()
    namespace: RedisCollectionNames = RedisCollectionNames()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        cli_parse_args=True,  # читать настройки из Cli
        case_sensitive=False,  # Если True, то учитываем регистр
    )

    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
