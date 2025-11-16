"""Module for storage config data"""

import logging

from pydantic import BaseModel
from pydantic_settings import BaseSettings

LOG_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggingConfig(BaseModel):
    log_level: int = logging.INFO
    log_format: str = LOG_FORMAT
    date_format: str = "%Y-%m-%d %H:%M:%S"


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
    logging: LoggingConfig = LoggingConfig()
    redis: RedisConfig = RedisConfig()


# noinspection PyArgumentList
settings = Settings()
