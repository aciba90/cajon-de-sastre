from abc import ABC, abstractmethod
from typing import Dict, Iterator
from app.domain.models import Word, Words


class Repository(ABC):
    """TODO"""

    @abstractmethod
    def update(self, word_dictionary: Words) -> None:
        ...

    @abstractmethod
    def list(self) -> Words:
        ...


class WordDictionaryMongoRepo(Repository):
    def __init__(self, session):
        self._session = session

    def update(self, word_dictionary: Words) -> None:
        payload = word_dictionary.to_dict()
        _id = payload.pop("_id")
        version = payload.pop("version")
        _ = self._session.client.app.wordsdictionary.update_one(
            {
                "_id": _id,
                "version": version
            },
            {
                "$set": payload, 
                "$inc": {"version": 1},
            },
            upsert=True,
            session=self._session, 
        )

    # def get(self, word: str) -> Word:
    #     word_data = self._session.client.app.words.find_one(
    #         {"word": word},
    #         {"_id": 0},
    #         session=self._session,
    #     )
    #     if word_data is None:
    #         # TODO handle
    #         pass
    #     return Word(**word_data)

    def list(self) -> Words:
        words = self._session.client.app.wordsdictionary.find_one(
            {"_id": "0"}, projection={"_id": False}, session=self._session
        )
        words_ = list(map(lambda w: Word(**w), words["words"]))
        return Words(words=words_, version=words["version"])
