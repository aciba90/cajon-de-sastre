"""Main FastAPI module."""

from itertools import product
from typing import Set

from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import app.config as Config
from app.models import Arrange, Graph, GraphConfig, Limit, Statistic
from app.services import compute_graph

tags_metadata = [
    {
        "name": "forms",
        "description": "Operations related to the form page.",
    },
    {
        "name": "graphs",
        "description": "Manage graph data.",
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
    summary="Handles form submition and redirects to the Graphs' page.",
    response_description="Rendered ´graphs.html´ page.",
)
async def handle_form(
    request: Request,
    statistics: Set[Statistic] = Form(...),
    limits: Set[Limit] = Form(...),
    arranges: Set[Arrange] = Form(...),
):
    """
    It injects the graph urls in to the page to be fetched and rendered with JavaScript.

    Params:

    - **statistics**: Set of instances of _Statistic_ to generate graphs with.
    - **limits**: Set of instances of _Limit_ to generate graphs with.
    - **arranges**: Set of instances of _Arrange_ to generate graphs with.
    """
    graph_configs = tuple(
        map(lambda x: GraphConfig(*x), product(statistics, limits, arranges))
    )
    base_url = app.url_path_for("get_graph")
    graph_urls = tuple(map(lambda g: g.build_url(base_url), graph_configs))
    context = {
        "request": request,
        "images": graph_urls,
        "width": Config.WIDTH,
        "height": Config.HEIGHT,
    }
    return templates.TemplateResponse("graphs.html", context)


@app.get(
    "/api/graphs",
    tags=["graphs"],
    summary="Retrieves graph data.",
    response_description="Graph data.",
    response_model=Graph,
)
async def get_graph(statistic: Statistic, limit: Limit, arrange: Arrange) -> Graph:
    """Params:

    - **statistic**: Instance of _Statistic_ telling what dependent variable to
    visualize.
    - **limit**: Instance of _Limit_ telling how many data points to visualize.
    - **arrange**: Instance of _Arrange_ telling how to sort the data points.
    """
    graph_config = GraphConfig(statistic=statistic, limit=limit, arrange=arrange)
    return compute_graph(graph_config)
