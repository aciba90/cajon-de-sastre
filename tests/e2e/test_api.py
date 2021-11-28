import pytest
import requests

from app import config


def post_to_words(word: str, postion: int) -> None:
    url = config.get_api_url()
    r = requests.post(f"{url}/words", json={"word": word, "position": postion})
    assert r.status_code == 201


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_returns_201_and_added_word():
    url = config.get_api_url()
    r = requests.post(f"{url}/words", json={"word": "asdf", "position": 0})
    assert r.status_code == 201


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_returns_200_patch_word():
    post_to_words(word="asdf", postion=1)

    url = config.get_api_url()
    r = requests.patch(f"{url}/words/asdf", json={"position": 5})
    assert r.status_code == 200, r.content
    assert r.json() == {'position': 0, 'word': 'asdf'}
