"""Module for storage config data"""

import logging
from typing import Final

from pydantic import BaseModel
from pydantic_settings import BaseSettings

LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

"""     ----- Настройка Redis -----     """
REDIS_DB_TOKENS: Final[int] = 1
REDIS_TOKENS_SET_NAME: Final[str] = "tokens"

REDIS_DB_USERS: Final[int] = 2

REDIS_DB_SHORT_URLS: Final[int] = 3
REDIS_SHORT_URLS_HASH_NAME: Final[str] = "short-urls"


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


class RedisConnectionConfig(BaseModel):
    host: str = "localhost"
    port: int = 6379


class RedisConfig(BaseModel):
    connection: RedisConnectionConfig = RedisConnectionConfig()


class Settings(BaseSettings):
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
