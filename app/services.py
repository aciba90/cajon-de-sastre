"""Service operations."""
import logging
from functools import cache
from io import BytesIO
from typing import Final, List

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

import app.config as Config
from app.models import GraphConfig, Statistic

matplotlib.use("agg")

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
    >>> from app.models import Limit, Arrange
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
