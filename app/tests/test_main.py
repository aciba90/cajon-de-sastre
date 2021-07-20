"""Integration tests"""
import pytest

import app.tests.config as Config
from app.tests.config import UrlPath, client


def test_form_get_200():
    """Tests that the main page is correct."""
    response = client.get("/nbastats")
    assert response.status_code == 200
    html = response.text
    assert "NBA Stats" in html
    assert "SUBMIT" in html
    assert "<form" in html


@pytest.mark.parametrize(
    ["statistic", "limit", "arrange", "name", "data_x", "data_y"],
    [
        (
            Config.POINTS,
            Config.FIVE,
            Config.ASCENDING,
            "PointsPG",
            [
                "Greg Whittington",
                "Ignas Brazdeikis",
                "Gary Clark",
                "Gary Clark",
                "Noah Vonleh",
            ],
            [0.0, 0.0, 0.0, 0.0, 0.0],
        ),
        (
            Config.POINTS,
            Config.TWENTY_FIVE,
            Config.ASCENDING,
            "PointsPG",
            [
                "Greg Whittington",
                "Ignas Brazdeikis",
                "Gary Clark",
                "Gary Clark",
                "Noah Vonleh",
                "Will Magnay",
                "Ashton Hagans",
                "Anzejs Pasecniks",
                "Theo Pinson",
                "Terrance Ferguson",
                "Jaylen Adams",
                "Jared Harper",
                "Chris Silva",
                "Jared Dudley",
                "Tyler Cook",
                "Ignas Brazdeikis",
                "Ty-Shon Alexander",
                "Brian Bowen II",
                "Rodions Kurucs",
                "Cameron Reynolds",
                "Keljin Blevins",
                "Nick Richards",
                "Vincent Poirier",
                "Kostas Antetokounmpo",
                "Jordan Bell",
            ],
            [
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.0,
                0.1,
                0.2,
                0.3,
                0.4,
                0.5,
                0.5,
                0.5,
                0.5,
                0.6,
                0.6,
                0.6,
                0.7,
                0.7,
                0.8,
                0.8,
                0.8,
                1.0,
            ],
        ),
        (
            Config.POINTS,
            Config.TEN,
            Config.DESCENDING,
            "PointsPG",
            [
                "Stephen Curry",
                "Bradley Beal",
                "Damian Lillard",
                "Joel Embiid",
                "Giannis Antetokounmpo",
                "Luka Doncic",
                "Zach LaVine",
                "Zion Williamson",
                "Kevin Durant",
                "Kyrie Irving",
            ],
            [32.0, 31.3, 28.7, 28.5, 28.1, 27.7, 27.4, 27.0, 26.9, 26.9],
        ),
    ],
)
def test_graph_get_200(statistic, limit, arrange, name, data_x, data_y):
    """Tests that the graph page is correct."""
    payload = {
        "statistic": statistic,
        "limit": limit,
        "arrange": arrange,
    }
    response = client.get(UrlPath.GRAPHS.get_url(), params=payload)
    assert response.status_code == 200
    data = response.json()

    expected_data = {"data_x": data_x, "data_y": data_y, "name": name}
    assert data == expected_data


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
    response = client.get(UrlPath.GRAPHS.get_url(), params=payload)
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
    response = client.post(UrlPath.NBA_STATS.get_url(), data=payload)
    assert response.status_code == 200
    html = response.text
    assert "html" in html
    assert "canvas" in html
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
    response = client.post(UrlPath.NBA_STATS.get_url(), data=payload)
    assert response.status_code == 422
