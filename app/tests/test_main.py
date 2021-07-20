"""Integration tests"""
import pytest

from app.tests.config import (
    UrlPath,
    client,
    POINTS,
    STEALS,
    REBOUNDS,
    ASSISTS,
    MINUTES,
    FIVE,
    TEN,
    FIFTEEN,
    TWENTY,
    TWENTY_FIVE,
    ASCENDING,
    DESCENDING,
)


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
            POINTS,
            FIVE,
            ASCENDING,
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
            POINTS,
            TWENTY_FIVE,
            ASCENDING,
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
            POINTS,
            TEN,
            DESCENDING,
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
        (
            STEALS,
            TEN,
            DESCENDING,
            "StealsPG",
            [
                "Jimmy Butler",
                "T.J. McConnell",
                "Khyri Thomas",
                "Victor Oladipo",
                "Larry Nance Jr.",
                "Draymond Green",
                "Fred VanVleet",
                "Victor Oladipo",
                "Jrue Holiday",
                "Matisse Thybulle",
            ],
            [2.08, 1.86, 1.8, 1.75, 1.74, 1.7, 1.67, 1.67, 1.64, 1.62],
        ),
        (
            REBOUNDS,
            TEN,
            DESCENDING,
            "ReboundsPG",
            [
                "Clint Capela",
                "Rudy Gobert",
                "Andre Drummond",
                "Jonas Valanciunas",
                "Domantas Sabonis",
                "Nikola Vucevic",
                "Nikola Vucevic",
                "Russell Westbrook",
                "Enes Kanter",
                "Giannis Antetokounmpo",
            ],
            [14.3, 13.5, 13.5, 12.5, 12.0, 11.8, 11.6, 11.5, 11.0, 11.0],
        ),
        (
            ASSISTS,
            TEN,
            DESCENDING,
            "AssistsPG",
            [
                "Russell Westbrook",
                "James Harden",
                "James Harden",
                "Trae Young",
                "Draymond Green",
                "Chris Paul",
                "Luka Doncic",
                "Nikola Jokic",
                "LeBron James",
                "Damian Lillard",
            ],
            [11.7, 10.9, 10.4, 9.4, 8.9, 8.9, 8.6, 8.3, 7.8, 7.5],
        ),
        (
            MINUTES,
            TWENTY_FIVE,
            ASCENDING,
            "MPG",
            [
                "Ignas Brazdeikis",
                "Theo Pinson",
                "Jared Harper",
                "Cameron Reynolds",
                "Ashton Hagans",
                "Gary Clark",
                "Chris Silva",
                "Jaylen Adams",
                "Udonis Haslem",
                "Noah Vonleh",
                "Brian Bowen II",
                "Greg Whittington",
                "Jalen Lecque",
                "Ty-Shon Alexander",
                "Rodions Kurucs",
                "Will Magnay",
                "Shaquille Harrison",
                "Elijah Hughes",
                "Nick Richards",
                "Robert Woodard II",
                "Malik Fitts",
                "Kostas Antetokounmpo",
                "Nate Darling",
                "Terrance Ferguson",
                "Norvel Pelle",
            ],
            [
                1.8,
                2.0,
                2.0,
                2.1,
                2.1,
                2.1,
                2.4,
                2.6,
                2.7,
                2.7,
                2.8,
                3.0,
                3.0,
                3.2,
                3.2,
                3.3,
                3.3,
                3.5,
                3.5,
                3.5,
                3.6,
                3.7,
                3.7,
                3.8,
                3.8,
            ],
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
        ("asdf", FIVE, ASCENDING),
        (POINTS, "asdf", DESCENDING),
        (STEALS, TEN, "asdf"),
        (STEALS, TWENTY, ""),
        (STEALS, TEN, TEN),
        (STEALS, DESCENDING, TEN),
    ],
)
def test_graph_get_422(statistic, limit, arrange):
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
        (POINTS, FIVE, ASCENDING),
        ([POINTS, STEALS], [TEN, FIVE], DESCENDING),
        (
            [ASSISTS, STEALS],
            [FIFTEEN, FIVE],
            [DESCENDING, ASCENDING],
        ),
        ([POINTS, POINTS], FIVE, ASCENDING),
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
        ("asdfa", FIVE, ASCENDING),
        ([], [TEN, FIVE], DESCENDING),
        (
            [ASSISTS, STEALS],
            ["45", FIVE],
            [DESCENDING, ASCENDING],
        ),
        ([], [], []),
        ("", "", ""),
    ],
)
def test_form_post_422(statistics, limits, arranges):
    """Tests the form submition with invalid data."""
    payload = {"statistics": statistics, "limits": limits, "arranges": arranges}
    response = client.post(UrlPath.NBA_STATS.get_url(), data=payload)
    assert response.status_code == 422
