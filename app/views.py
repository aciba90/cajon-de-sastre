"""CQRS pattern"""

from pymongo.mongo_client import MongoClient

from pymongo import MongoClient, ASCENDING


def list_words(client: MongoClient):
    result = client.app.word.find(
        {},
        projection={"_id": False, "word": True},
        sort=[("position", ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))


def get_anagrams(anagram_hash: int, client: MongoClient):
    result = client.app.word.find(
        {"anagram_hash": anagram_hash},
        projection={"_id": False, "word": True},
        sort=[("position", ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))
