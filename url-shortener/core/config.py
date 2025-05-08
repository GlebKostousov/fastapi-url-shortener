import logging
from pathlib import Path
from typing import Final

BASE_DIR = Path(__file__).resolve().parent.parent
SHORT_URLS_STORAGE_FILE_PATH = BASE_DIR / "short-urls.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: Final[str] = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "mFOcFcH4FWqEfH-88jhCTbVxN6c",
        "PkaVw5QFUmypE9Gwsf2y2g",
        "T2FP-VqUmzfg5nZ01ZxrCA",
    }
)
