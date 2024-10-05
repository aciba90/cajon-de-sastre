"""Test config."""
from fastapi.testclient import TestClient

from app.main import (
    Arrange as _Arrange,
    Limit as _Limit,
    Statistic as _Statistic,
)
from app.main import app as _app
from enum import IntEnum, auto


client = TestClient(_app)

ASCENDING = _Arrange.ASCENDING
DESCENDING = _Arrange.DESCENDING

FIVE = _Limit.FIVE
TEN = _Limit.TEN
FIFTEEN = _Limit.FIFTEEN
TWENTY = _Limit.TWENTY
TWENTY_FIVE = _Limit.TWENTY_FIVE

POINTS = _Statistic.POINTS
ASSISTS = _Statistic.ASSISTS
REBOUNDS = _Statistic.REBOUNDS
STEALS = _Statistic.STEALS
MINUTES = _Statistic.MINUTES


class UrlPath(IntEnum):
    """Urls's enumerartion."""

    NBA_STATS = auto()
    GRAPHS = auto()

    def get_url(self) -> str:
        """Gets the associated url path.

        :return: Url path associated to ´self´.
        """
        if self == self.NBA_STATS:
            return "/nbastats"
        elif self == self.GRAPHS:
            return "/api/graphs"
        raise NotImplementedError
