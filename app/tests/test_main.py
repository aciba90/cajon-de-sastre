"""Integration tests"""
from itertools import product

import pytest
from fastapi.testclient import TestClient

from app.main import Arrange, Limit, Statistic
from app.main import app as app_

client = TestClient(app_)


def test_form_get_200():
    """Tests that the main page is correct."""
    response = client.get("/nbastats")
    assert response.status_code == 200
    html = response.text
    assert "NBA Stats" in html
    assert "SUBMIT" in html
    assert "<form" in html


ALL_GRAPH_CONFIGS = list(
    product(
        map(lambda x: x.value, Statistic),
        map(lambda x: x.value, Limit),
        map(lambda x: x.value, Arrange),
    )
)


@pytest.mark.parametrize(["statistic", "limit", "arrange"], ALL_GRAPH_CONFIGS)
def test_graph_get_200(statistic, limit, arrange):
    """Tests that the graph page is correct."""
    payload = {
        "statistic": statistic,
        "limit": limit,
        "arrange": arrange,
    }
    response = client.get("/graphs", params=payload)
    assert response.status_code == 200
    assert b"\x89PNG" in response.content


@pytest.mark.parametrize(
    ["statistic", "limit", "arrange"],
    [
        ("asdf", "5", "ascending"),
        ("points", "asdf", "descending"),
        ("steals", "10", "asdf"),
    ],
)
def test_graph_get_404(statistic, limit, arrange):
    """Tests that the graph page is correct."""
    payload = {
        "statistic": statistic,
        "limit": limit,
        "arrange": arrange,
    }
    response = client.get("/graphs", params=payload)
    assert response.status_code == 422


@pytest.mark.parametrize(
    ["statistics", "limits", "arranges"],
    [
        ("points", "5", "ascending"),
        (["points", "steals"], ["10", "5"], "descending"),
        (["assists", "steals"], ["15", "5"], ["descending", "ascending"]),
    ],
)
def test_form_post_200(statistics, limits, arranges):
    """Tests the form submition."""
    payload = {"statistics": statistics, "limits": limits, "arranges": arranges}
    response = client.post("/nbastats", data=payload)
    assert response.status_code == 200
    html = response.text
    assert "html" in html
    assert "img" in html
    assert "graph" in html


@pytest.mark.parametrize(
    ["statistics", "limits", "arranges"],
    [
        ("asdfa", "5", "ascending"),
        ([], ["10", "5"], "descending"),
        (["assists", "steals"], ["45", "5"], ["descending", "ascending"]),
        ([], [], []),
        ("", "", ""),
    ],
)
def test_form_post_400(statistics, limits, arranges):
    """Tests the form submition with invalid data."""
    payload = {"statistics": statistics, "limits": limits, "arranges": arranges}
    response = client.post("/nbastats", data=payload)
    assert response.status_code == 422
