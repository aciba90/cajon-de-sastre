from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from itertools import product
from typing import Set

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
    POINTS = "points"
    ASSISTS = "assists"
    REBOUNDS = "rebounds"
    STEALS = "steals"
    MINUTES = "minutes"

    def get_column_name(self) -> str:
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
    FIVE = "5"
    TEN = "10"
    FIFTEEN = "15"
    TWENTY = "20"
    TWENTY_FIVE = "25"

    def get_limit(self) -> int:
        return int(self.value)


class Arrange(str, Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"

    def is_ascending(self) -> bool:
        return self == self.ASCENDING


@app.get("/nbastats")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/nbastats")
def compute_stats_controller(
    request: Request,
    statistics: Set[Statistic] = Form(...),
    limits: Set[Limit] = Form(...),
    arranges: Set[Arrange] = Form(...),
):
    """
    TODO doc, validation
    """

    def adapt_to_set(value, final_type):
        if not isinstance(value, set):
            return {final_type(value)}
        return value

    statistics = adapt_to_set(statistics, Statistic)
    limits = adapt_to_set(limits, Limit)
    arranges = adapt_to_set(arranges, Arrange)

    graph_configs = tuple(
        map(lambda x: GraphConfig(*x), product(statistics, limits, arranges))
    )
    images = tuple(
        app.url_path_for(
            "graphs_controller",
            statistic=graph_config.statistic.value,
            limit=graph_config.limit.value,
            arrange=graph_config.arrange.value,
        )
        for graph_config in graph_configs
    )
    return templates.TemplateResponse(
        "graph.html",
        {
            "request": request,
            "images": images,
        },
    )


@app.get("/graphs/{statistic}/{limit}/{arrange}")
def graphs_controller(statistic: Statistic, limit: Limit, arrange: Arrange):
    graph_config = GraphConfig(statistic=statistic, limit=limit, arrange=arrange)
    image = compute_graph(graph_config)
    # TODO add nocache headers
    # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate,
    # max-age=0'
    return StreamingResponse(image, media_type="image/png")


@dataclass(frozen=True)
class GraphConfig:
    """TODO"""

    statistic: Statistic
    limit: Limit
    arrange: Arrange

    def get_graphs_info(self):
        return product(
            map(self.statistic, lambda x: x.value),
            map(self.limit, lambda x: x.value),
            map(self.arrange, lambda x: x.value),
        )


def _load_csv() -> pd.DataFrame:
    """TODO"""
    return pd.read_csv(Config.CSV_PATH)


def compute_graph(graph_config: GraphConfig) -> BytesIO:
    """TODO"""
    df = _load_csv()

    y_column_name = graph_config.statistic.get_column_name()
    is_ascending = graph_config.arrange.is_ascending()
    n_items = graph_config.limit.get_limit()

    df = df[[Config.FULL_NAME_COL, y_column_name]].sort_values(
        axis=0, by=y_column_name, ascending=is_ascending
    )
    fig, ax = plt.subplots(
        dpi=Config.DPI, figsize=(Config.WIDTH_INCHES, Config.HEIGHT_INCHES)
    )
    df.iloc[:n_items, :].plot(Config.FULL_NAME_COL, y_column_name, kind="bar", ax=ax)
    b = BytesIO()
    fig.savefig(
        b,
        format=Config.IMAGE_FORMAT,
        bbox_inches="tight",  # To not cut x's labels.
    )
    plt.close(fig)
    b.seek(0)
    return b
