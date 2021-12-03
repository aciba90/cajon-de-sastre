"""CQRS pattern"""
from pymongo import MongoClient, ASCENDING
from typing import List


def list_words(client: MongoClient) -> List[str]:
    """List existing words ordered by position"""
    result = client.app.word.find(
        {},
        projection={"_id": False, "word": True},
        sort=[("position", ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))


def get_anagrams(anagram_hash: int, client: MongoClient) -> List[str]:
    """Gets the anagram set associated to `anagram_hash`."""
    result = client.app.word.find(
        {"anagram_hash": anagram_hash},
        projection={"_id": False, "word": True},
        sort=[("position", ASCENDING)],
    )
    return list(map(lambda w: w["word"], result))
