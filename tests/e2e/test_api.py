import pytest
import requests

from app import config


def post_to_words(word: str, position: int) -> None:
    url = config.get_api_url()
    r = requests.post(f"{url}/words", json={"word": word, "position": position})
    assert r.status_code == 201, r.content


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_returns_201_and_added_word():
    url = config.get_api_url()
    r = requests.post(f"{url}/words", json={"word": "asdf", "position": 0})
    assert r.status_code == 201, r.content


@pytest.mark.xfail
@pytest.mark.usefixtures("mongo_db")
def test_happy_path_returns_200_patch_word():
    post_to_words(word="asdf", position=1)

    url = config.get_api_url()
    r = requests.patch(f"{url}/words/asdf", json={"position": 5})
    assert r.status_code == 200, r.content
    assert r.json() == {'position': 5, 'word': 'asdf'}


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_returns_200_list_words():
    post_to_words(word="a", position=1)
    post_to_words(word="b", position=0)

    url = config.get_api_url()
    r = requests.get(f"{url}/words")
    assert r.status_code == 200, r.content
    words = r.json()["data"]
    assert words == ["b", "a"]
