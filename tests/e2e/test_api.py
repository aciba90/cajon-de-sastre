import pytest
import requests

from app import config
from . import api_client


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_example_full():
    api_client.post_to_words("cosa", 0)
    api_client.post_to_words("caso", 1)
    api_client.post_to_words("paco", 2)
    api_client.post_to_words("pepe", 3)
    api_client.post_to_words("Málaga", 4)
    r = api_client.get_to_words()
    assert r.json() == {"data": ["cosa", "caso", "paco", "pepe", "Málaga"]}, r.json

    r = api_client.post_to_words("calle", 3)
    assert r.json() == {"word": "calle", "position": 3}

    r = api_client.get_to_words()
    assert r.json() == {
        "data": ["cosa", "caso", "paco", "calle", "pepe", "Málaga"]
    }, r.json

    r = api_client.patch_to_words("calle", 5)
    assert r.json() == {"word": "calle", "position": 5}, r.json

    r = api_client.get_to_words()
    assert r.json() == {
        "data": ["cosa", "caso", "paco", "pepe", "calle", "Málaga"]
    }, r.json

    r = api_client.get_anagrams("asco")
    assert r.json() == {"data": ["cosa", "caso"]}, r.json

    r = api_client.delete_to_words("calle")

    r = api_client.get_to_words()
    assert r.json() == {"data": ["cosa", "caso", "paco", "pepe", "Málaga"]}, r.json


@pytest.mark.usefixtures("mongo_db")
def test_add_repeated_word():
    url = config.get_api_url()
    api_client.post_to_words("cosa", 0)
    r = requests.post(f"{url}/words", json={"word": "cosa", "position": 0})
    assert r.status_code == 400


@pytest.mark.usefixtures("mongo_db")
def test_patch_non_existing_word():
    url = config.get_api_url()
    r = requests.patch(f"{url}/words/asdfasdfasd", json={"position": 0})
    assert r.status_code == 400, str(r.content)


@pytest.mark.usefixtures("mongo_db")
def test_patch_word_two_times_repeated():
    url = config.get_api_url()
    api_client.post_to_words("cosa", 0)
    r = requests.patch(f"{url}/words/cosa", json={"position": 0})
    assert r.status_code == 200
    r = requests.patch(f"{url}/words/cosa", json={"position": 0})
    assert r.status_code == 400, str(r.content)
