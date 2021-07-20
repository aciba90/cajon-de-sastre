"""Service operations."""
from functools import cache
from typing import Final, List

import pandas as pd

import app.config as Config
from app.models import Graph, GraphConfig, Statistic

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
def compute_graph(graph_config: GraphConfig) -> Graph:
    """TODO"""
    df = _read_csv()

    y_column_name = graph_config.statistic.get_column_name()
    is_ascending = graph_config.arrange.is_ascending
    n_items = graph_config.limit.get_limit()

    df = df[[Config.FULL_NAME_COL, y_column_name]].sort_values(
        axis=0, by=y_column_name, ascending=is_ascending
    )
    x = df.iloc[:n_items, 0].to_numpy().tolist()
    y = df.iloc[:n_items, 1].to_numpy().tolist()
    return Graph(name=y_column_name, data_x=x, data_y=y)
