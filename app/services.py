from __future__ import annotations

from typing import Dict

import pymongo
from pymongo import MongoClient
from functools import lru_cache


_lookup: Dict[str, int] = {
    "A": 2,
    "a": 2,
    "B": 3,
    "b": 3,
    "C": 5,
    "c": 5,
    "D": 7,
    "d": 7,
    "E": 11,
    "e": 11,
    "F": 13,
    "f": 13,
    "G": 17,
    "g": 17,
    "H": 19,
    "h": 19,
    "I": 23,
    "i": 23,
    "J": 29,
    "j": 29,
    "K": 31,
    "k": 31,
    "L": 37,
    "l": 37,
    "M": 41,
    "m": 41,
    "N": 43,
    "n": 43,
    "O": 47,
    "o": 47,
    "P": 53,
    "p": 53,
    "Q": 59,
    "q": 59,
    "R": 61,
    "r": 61,
    "S": 67,
    "s": 67,
    "T": 71,
    "t": 71,
    "U": 73,
    "u": 73,
    "V": 79,
    "v": 79,
    "W": 83,
    "w": 83,
    "X": 89,
    "x": 89,
    "Y": 97,
    "y": 97,
    "Z": 101,
    "z": 101,
}



@lru_cache(maxsize=int(1e3))
def _compute_anagram_hash(word: str) -> int:
    """[summary]

    Example:
    --------
    >>> _compute_anagram_hash("asdf")
    12194
    >>> _compute_anagram_hash("fdas")
    12194
    >>> _compute_anagram_hash("aas")
    268

    :param word: [description]
    :type word: str
    :return: [description]
    :rtype: int
    """
    anagram_hash = 1
    for letter in word:
        anagram_hash *= _lookup.get(letter, 1)
    return anagram_hash


def add_word(word: str, position: int, client: MongoClient):
    existing_word = client.app.word.find_one({"word": word})
    if existing_word is None:
        client.app.word.update_many(
            {"position": {"$gte": position}}, {"$inc": {"position": 1}}
        )
        anagram_hash = _compute_anagram_hash(word)
        client.app.word.insert_one({"word": word, "position": position, "anagram_hash": anagram_hash})
    return {"word": word, "position": position}, 201


def update_word(word: str, position: int, client: MongoClient):
    lock_version = client.app.lock.find_one({"_id": 0})
    client.app.lock.update_one(
        {"_id": 0, "version": lock_version["version"]},
        {"$inc": {"version": 1}},
    )
    position_old = client.app.word.find_one({"word": word})["position"]
    client.app.word.update_many(
        {"position": {"$gte": position_old}}, {"$inc": {"position": 1}},
    )
    client.app.word.update_one(
        {"word": word}, {"$set": {"position": position}}
    )
    return word, position


def delete_word(word: str, client: MongoClient):
    client.app.word.delete_one({"word": word})


def list_words(client: MongoClient):
    result = client.app.word.find(
        {},
        projection={"_id": False, "word": True},
        sort=[("position", pymongo.ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))


def get_anagrams(word, client):
    anagram_hash = _compute_anagram_hash(word)
    result = client.app.word.find(
        {"anagram_hash": anagram_hash},
        projection={"_id": False, "word": True},
        sort=[("position", pymongo.ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))
