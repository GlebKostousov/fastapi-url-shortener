# https://github.com/GlebKostousov/List-of-the-movie

import logging
from os import getenv
from typing import Final

LOG_LEVEL = logging.INFO
LOG_FORMAT: Final[str] = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


"""     ----- Настройка Redis -----     """
REDIS_HOST: Final[str] = "localhost"
REDIS_PORT: Final[int] = int(getenv("REDIS_PORT", "0")) or 6379
REDIS_DB_TOKENS: Final[int] = 1
REDIS_TOKENS_SET_NAME: Final[str] = "tokens"

REDIS_DB_USERS: Final[int] = 2

REDIS_DB_SHORT_URLS: Final[int] = 3
REDIS_SHORT_URLS_HASH_NAME: Final[str] = "short-urls"
