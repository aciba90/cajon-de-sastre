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

    def update(self, word: Word) -> None:
        word_str = word.word
        version = word.version or 1
        word = self._session.client.app.words.find_one({"word": word.word})

        _ = self._session.client.app.words.update_many(
            {
                "word": word_str,
                "version": version
            },
            {
                "$set": payload, 
                "$inc": {"version": 1},
            },
            upsert=True,
            session=self._session, 
        )


    def list(self) -> Words:
        words = list(self._session.client.app.words.find(
            {}, projection={"_id": False}, session=self._session
        ))
        words_ = list(map(lambda w: Word(**w), words))
        return Words(words=words_, version=words["version"])
