"""APP Configuration"""

import os
from pathlib import Path
from typing import Final
import logging

_CSV = os.getenv("APP_CSV_PATH")
assert _CSV is not None, "Define APP_CSV_PATH env variable!"
CSV_PATH: Final[Path] = Path(_CSV)
assert CSV_PATH.is_file(), "CSV data file not found!"

FULL_NAME_COL: Final[str] = "FULL NAME"
WIDTH: Final[int] = int(os.getenv("APP_WIDTH", 400))
HEIGHT: Final[int] = int(os.getenv("APP_HEIGHT", 400))
LOG_LEVEL: Final[str] = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
