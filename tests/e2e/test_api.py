import pytest
import requests

from app import config
from . import api_client


@pytest.mark.usefixtures("mongo_db")
def test_happy_path_example_full():
    url = config.get_api_url()
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
