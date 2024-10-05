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
    >>> df.describe()
                  MPG    PointsPG  ReboundsPG   AssistsPG    StealsPG
    count  626.000000  626.000000  626.000000  626.000000  626.000000
    mean    19.528435    8.716134    3.590575    1.949201    0.611550
    std      9.362613    6.411011    2.404547    1.846157    0.399788
    min      1.800000    0.000000    0.000000    0.000000    0.000000
    25%     12.100000    4.000000    1.900000    0.700000    0.300000
    50%     19.500000    7.200000    3.200000    1.400000    0.580000
    75%     27.300000   11.975000    4.800000    2.500000    0.877500
    max     37.600000   32.000000   14.300000   11.700000    2.080000

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
    """Computes the graph associated with ´graph_config´.

    Example:
    --------
    >>> from app.models import Limit, Arrange
    >>> graph_config = GraphConfig(
    ...     statistic=Statistic.POINTS, limit=Limit.FIVE, arrange=Arrange.ASCENDING
    ... )
    >>> compute_graph(graph_config)
    Graph(name='PointsPG', data_x=['Greg Whittington', 'Ignas Brazdeikis', \
'Gary Clark', 'Gary Clark', 'Noah Vonleh'], data_y=[0.0, 0.0, 0.0, 0.0, 0.0])

    :param graph_config: Instance of ´GraphConfig´ that determines what kind of graph to
    generate.
    :return: Data needed to visualize the graph.
    """
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
