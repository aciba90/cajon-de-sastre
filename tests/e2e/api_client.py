from app import config
import requests


url = config.get_api_url()


def post_to_words(word: str, position: int):
    r = requests.post(f"{url}/words", json={"word": word, "position": position})
    assert r.status_code == 201, r.content
    return r


def get_to_words():
    r = requests.get(f"{url}/words")
    assert r.status_code == 200, r.content
    return r


def patch_to_words(word, position):
    r = requests.patch(f"{url}/words/{word}", json={"position": position})
    assert r.status_code == 200, r.content
    return r


def delete_to_words(word):
    r = requests.delete(f"{url}/words/{word}")
    assert r.status_code == 204, r.content
    return r


def get_anagrams(word):
    r = requests.get(f"{url}/words/{word}/anagrams")
    assert r.status_code == 200, r.content
    return r
