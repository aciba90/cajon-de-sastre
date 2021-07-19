"""APP Configuration"""

import os
from pathlib import Path
from typing import Final


def _to_inches(pixels: int, dpi: float) -> float:
    """Pixels ÷ DPI = Inches"""
    return pixels / dpi


_CSV = os.getenv("APP_CSV_PATH")
assert _CSV is not None, "Define APP_CSV_PATH env variable!"
CSV_PATH: Final[Path] = Path(_CSV)
assert CSV_PATH.is_file(), "CSV data file not found!"

FULL_NAME_COL: Final[str] = "FULL NAME"
WIDTH: Final[int] = int(os.getenv("APP_WIDTH", 400))
HEIGHT: Final[int] = int(os.getenv("APP_HEIGHT", 400))
DPI: Final[float] = float(os.getenv("APP_DPI", 96))
WIDTH_INCHES: Final[float] = _to_inches(WIDTH, DPI)
HEIGHT_INCHES: Final[float] = _to_inches(HEIGHT, DPI)
IMAGE_FORMAT: Final[str] = os.getenv("APP_IMAGE_FORMAT", "png")
