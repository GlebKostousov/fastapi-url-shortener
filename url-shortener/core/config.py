# https://github.com/GlebKostousov/List-of-the-movie

import logging
from pathlib import Path
from typing import Final

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILE_PATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: Final[str] = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


# Only for demo
# No real users in code
USERS_DB: dict[str, str] = {
    # username: password
    "sam": "password",
    "bob": "qwerty",
}
"""     ----- Настройка Redis -----     """
REDIS_HOST: Final[str] = "localhost"
REDIS_PORT: Final[int] = 6379
REDIS_DB_TOKENS: Final[int] = 1

REDIS_TOKENS_SET_NAME: Final[str] = "tokens"
