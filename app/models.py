"""Contains Models"""
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Dict, List
from urllib.parse import urlencode

from pydantic import BaseModel


class Statistic(str, Enum):
    """Statistic's enumerartion."""

    POINTS = "points"
    ASSISTS = "assists"
    REBOUNDS = "rebounds"
    STEALS = "steals"
    MINUTES = "minutes"

    def get_column_name(self) -> str:
        """Gets the associated column name to `self` in the dataframe.

        Example:
        --------
        >>> Statistic.POINTS.get_column_name()
        'PointsPG'
        >>> for stat in Statistic:
        ...     _ = stat.get_column_name()

        :return: Column name associated to ´self´.
        """
        if self == self.POINTS:
            return "PointsPG"
        elif self == self.ASSISTS:
            return "AssistsPG"
        elif self == self.REBOUNDS:
            return "ReboundsPG"
        elif self == self.STEALS:
            return "StealsPG"
        elif self == self.MINUTES:
            return "MPG"
        raise NotImplementedError


class Limit(str, Enum):
    """Limit's enumerartion."""

    FIVE = "5"
    TEN = "10"
    FIFTEEN = "15"
    TWENTY = "20"
    TWENTY_FIVE = "25"

    def get_limit(self) -> int:
        """Gets the numeric value associated to ´self´.

        Example:
        --------
        >>> Limit.FIVE.get_limit()
        5

        :return: Integer limit value assciated to ´self´.
        """
        return int(self.value)


class Arrange(str, Enum):
    """Arrange's enumerartion."""

    ASCENDING = "ascending"
    DESCENDING = "descending"

    @property
    def is_ascending(self) -> bool:
        """Determines if ´self´ is ascending

        Example:
        --------
        >>> Arrange.ASCENDING.is_ascending
        True
        >>> Arrange.DESCENDING.is_ascending
        False

        :return: True if ´self´ is ascending, False otherwise.
        """
        return self == self.ASCENDING


@dataclass(frozen=True)
class GraphConfig:
    """Stores a Graph configuration.

    >>> GraphConfig(
    ...     statistic=Statistic.POINTS, limit=Limit.FIVE, arrange=Arrange.ASCENDING
    ... )
    GraphConfig(statistic=<Statistic.POINTS: 'points'>, limit=<Limit.FIVE: '5'>, \
arrange=<Arrange.ASCENDING: 'ascending'>)
    """

    statistic: Statistic
    limit: Limit
    arrange: Arrange

    def to_dict(self) -> Dict:
        """
        Converts ´self´ to a dict, extracting the enum values of the values.

        Example:
        --------
        >>> graph_config = GraphConfig(
        ...     statistic=Statistic.POINTS, limit=Limit.FIVE, arrange=Arrange.ASCENDING
        ... )
        >>> graph_config.to_dict()
        {'statistic': 'points', 'limit': '5', 'arrange': 'ascending'}

        :return: Dict containing attribute names as keys and the enum values of the
        attributes as values.
        """
        # return asdict(self)
        return {k: v.value for k, v in asdict(self).items()}

    def build_url(self, base_url: str) -> str:
        """Builds a url by joining `base_url` and `self`, enconded as query params.

        Example:
        --------
        >>> graph_config = GraphConfig(
        ...     statistic=Statistic.POINTS, limit=Limit.FIVE, arrange=Arrange.ASCENDING
        ... )
        >>> graph_config.build_url("<base_url>")
        '<base_url>?statistic=points&limit=5&arrange=ascending'

        :param base_url: Base url to compose with.
        :return: Composed url.
        """
        return f"{base_url}?{urlencode(self.to_dict())}"

    def get_id(self) -> str:
        """TODO"""
        return self.build_url("graph")


class Graph(BaseModel):
    name: str
    data_x: List[str]
    data_y: List[float]
