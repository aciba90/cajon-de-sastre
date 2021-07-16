from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from pathlib import Path
from typing import Final

import matplotlib.pyplot as plt
import pandas as pd
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class Config:
    CSV_PATH = Path(os.getenv("APP_CSV_PATH", ""))
    FULL_NAME_COL: Final[str] = "FULL NAME"


assert Config.CSV_PATH.is_file(), "CSV data file not found!"


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
    statistic: Statistic = Form(...),
    limit: Limit = Form(...),
    arrange: Arrange = Form(...),
):
    """
    TODO doc, validation
    """
    graph_config = GraphConfig(statistic=statistic, limit=limit, arrange=arrange)
    image = app.url_path_for(
        "graphs_controller",
        statistic=graph_config.statistic.value,
        limit=graph_config.limit.value,
        arrange=graph_config.arrange.value,
    )
    return templates.TemplateResponse(
        "graph.html",
        {
            "request": request,
            "image": image,
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
    df.iloc[:n_items, :].plot(Config.FULL_NAME_COL, y_column_name, kind="bar")

    b = BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return b
