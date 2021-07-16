from __future__ import annotations

import os
from dataclasses import dataclass
from enum import Enum
from io import BytesIO
from pathlib import Path

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


assert Config.CSV_PATH.is_file(), "CSV data file not found!"


class Statistic(str, Enum):
    POINTS = "points"
    ASSISTS = "assists"
    REBOUNDS = "rebounds"
    STEALS = "steals"
    MINUTES = "minutes"


class Limit(str, Enum):
    FIVE = "5"
    TEN = "10"
    FIFTEEN = "15"
    TWENTY = "20"
    TWENTY_FIVE = "25"


class Arrange(str, Enum):
    ASCENDING = "ascending"
    DESCENDING = "descending"


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
    image = compute_stats(graph_config)
    # TODO add nocache headers
    # response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate,
    # max-age=0'
    return StreamingResponse(image, media_type="image/png")


@dataclass
class GraphConfig:
    """TODO"""

    statistic: Statistic
    limit: Limit
    arrange: Arrange


def _load_csv() -> pd.DataFrame:
    """TODO"""
    df = pd.read_csv(Config.CSV_PATH)
    return df


def compute_stats(graph_config: GraphConfig) -> BytesIO:
    """TODO"""
    df = _load_csv()
    df.iloc[:10, :].plot("FULL NAME", "AGE", kind="bar", title="title")
    b = BytesIO()
    plt.savefig(b, format="png")
    b.seek(0)
    return b
