"""Main FastAPI module."""

from __future__ import annotations

from io import BytesIO
from itertools import product
from typing import Set

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.responses import StreamingResponse

import app.config as Config
from app.models import Arrange, GraphConfig, Limit, Statistic
from app.services import compute_graph

tags_metadata = [
    {
        "name": "forms",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "graphs",
        "description": "Manage items. So _fancy_ they have their own docs.",
    },
]

app = FastAPI(
    title="NBAStats",
    description="Web app to visualize NBA statistics.",
    version="0.1.0",
    openapi_tags=tags_metadata,
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get(
    "/nbastats",
    tags=["forms"],
    summary="Renders the Graph Form page.",
    response_description="The rendered page.",
)
async def render_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})


@app.post(
    "/nbastats",
    tags=["forms"],
    summary="Handles form submition and redirec to the Graphs' page.",
    response_description="Rendered ´graphs.html´ page.",
)
async def handle_form(
    request: Request,
    statistics: Set[Statistic] = Form(...),
    limits: Set[Limit] = Form(...),
    arranges: Set[Arrange] = Form(...),
):
    """Params:
    - **statistics**: Set of instances of _Statistic_ to generate graphs with.
    - **limits**: Set of instances of _Limit_ to generate graphs with.
    - **arranges**: Set of instances of _Arrange_ to generate graphs with.
    """
    graph_configs = tuple(
        map(lambda x: GraphConfig(*x), product(statistics, limits, arranges))
    )
    base_url = app.url_path_for("get_graph")
    graph_urls = tuple(map(lambda g: g.build_url(base_url), graph_configs))
    return templates.TemplateResponse(
        "graphs.html",
        {
            "request": request,
            "images": graph_urls,
            "width": Config.WIDTH,
            "height": Config.HEIGHT,
        },
    )


@app.get(
    "/graphs",
    tags=["graphs"],
    summary="Retrieves a graph image.",
    response_description="Computed graph image.",
)
def get_graph(statistic: Statistic, limit: Limit, arrange: Arrange):
    """Params:

    - **statistic**: Instance of _Statistic_ telling what dependent variable to
    visualize.
    - **limit**: Instance of _Limit_ telling how many data points to visualize.
    - **arrange**: Instance of _Arrange_ telling how to sort the data points.
    """
    graph_config = GraphConfig(statistic=statistic, limit=limit, arrange=arrange)
    image_id = graph_config.get_id()
    image = compute_graph(image_id, graph_config)
    image_buffer = BytesIO(image)
    return StreamingResponse(image_buffer, media_type="image/png")
