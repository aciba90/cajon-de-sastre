"""Main FastAPI module."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass
from enum import Enum
from functools import cache
from io import BytesIO
from itertools import product
from typing import Dict, Final, List, Set

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

import app.config as Config

matplotlib.use("agg")

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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


@app.get("/nbastats")
def render_form(request: Request):
    """Renders the graph form page.

    :param request: The request.
    :return: Rendered ´form.html´ page.
    """
    return templates.TemplateResponse("form.html", {"request": request})


@app.post("/nbastats")
def handle_form(
    request: Request,
    statistics: Set[Statistic] = Form(...),
    limits: Set[Limit] = Form(...),
    arranges: Set[Arrange] = Form(...),
):
    """Handles form submition redirecting to the graphs page.

    :param request: The request.
    :param statistics: Set of instances of ´Statistic´ to generate graphs with.
    :param limits: Set of instances of Limit to generate graphs with.
    :param arranges: Set of instances of ´Arrange´ to generate graphs with.
    :return: Rendered ´graphs.html´ page.
    """
    graph_configs = tuple(
        map(lambda x: GraphConfig(*x), product(statistics, limits, arranges))
    )
    images = tuple(
        app.url_path_for("get_graph", **graph_config.to_dict())
        for graph_config in graph_configs
    )
    return templates.TemplateResponse(
        "graphs.html",
        {
            "request": request,
            "images": images,
            "width": Config.WIDTH,
            "height": Config.HEIGHT,
        },
    )


@app.get("/graphs/{statistic}/{limit}/{arrange}")
def get_graph(statistic: Statistic, limit: Limit, arrange: Arrange):
    """Retrieves a graph image.

    :param statistic: Instance of ´Statistic´ telling what dependent variable to
    visualize.
    :param limit: Instance of ´Limit´ telling how many data points to visualize.
    :param arrange: Instance of ´arrange´ telling how to sort the data points.
    :return: Computed streamed graph image.
    """
    graph_config = GraphConfig(statistic=statistic, limit=limit, arrange=arrange)
    image = compute_graph(graph_config)
    image_buffer = BytesIO(image)
    return StreamingResponse(image_buffer, media_type="image/png")


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


_ALL_COLS: Final[List[str]] = [Config.FULL_NAME_COL] + list(
    map(lambda x: x.get_column_name(), Statistic)
)


def _read_csv() -> pd.DataFrame:
    """Reads the csv.

    Example:
    --------
    >>> df = _read_csv()
    >>> df.shape
    (626, 6)
    >>> df.dtypes
    FULL NAME      object
    MPG           float64
    PointsPG      float64
    ReboundsPG    float64
    AssistsPG     float64
    StealsPG      float64
    dtype: object

    :return: Instance of ´pd.DataFrame´ containing the data.
    """
    return pd.read_csv(
        Config.CSV_PATH,
        sep=",",
        header=0,
        usecols=_ALL_COLS,
    )


@cache
def compute_graph(graph_config: GraphConfig) -> bytes:
    """Computes the graph associated with ´graph_config´.

    Example:
    --------
    >>> graph_config = GraphConfig(
    ...     statistic=Statistic.POINTS, limit=Limit.FIVE, arrange=Arrange.ASCENDING
    ... )
    >>> compute_graph(graph_config)
    b'\x89PNG...'

    :param graph_config: Instance of ´GraphConfig´ that determines what kind of graph to
    generate.
    :return: Computed graph in bytes.
    """
    logging.info(f"Compute graph {graph_config}")
    df = _read_csv()

    y_column_name = graph_config.statistic.get_column_name()
    is_ascending = graph_config.arrange.is_ascending
    n_items = graph_config.limit.get_limit()

    df = df[[Config.FULL_NAME_COL, y_column_name]].sort_values(
        axis=0, by=y_column_name, ascending=is_ascending
    )
    fig, ax = plt.subplots(
        dpi=Config.DPI, figsize=(Config.WIDTH_INCHES, Config.HEIGHT_INCHES)
    )
    df.iloc[:n_items, :].plot(Config.FULL_NAME_COL, y_column_name, kind="bar", ax=ax)
    buffer = BytesIO()
    fig.savefig(
        buffer,
        format=Config.IMAGE_FORMAT,
        bbox_inches="tight",  # To not cut x's labels.
    )
    plt.close(fig)
    return buffer.getvalue()
