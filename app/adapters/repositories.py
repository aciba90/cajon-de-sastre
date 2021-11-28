from abc import ABC, abstractmethod
from typing import Dict, Iterator
from app.domain.models import Word


class WordRepo(ABC):
    """TODO"""

    @abstractmethod
    def add(self, word: Word) -> None:
        ...

    @abstractmethod
    def get(self, word: Word) -> Word:
        ...

    @abstractmethod
    def list(self) -> Iterator[Word]:
        ...


class WordMongoRepo(WordRepo):
    def __init__(self, session):
        self._session = session

    def add(self, word: Word) -> None:
        payload = word.to_dict()
        _ = self._session.client.app.words.insert_one(payload, session=self._session)

    def get(self, word: str) -> Word:
        word_data = self._session.client.app.words.find_one(
            {"word": word},
            {"_id": 0},
            session=self._session,
        )
        if word_data is None:
            # TODO handle
            pass
        return Word(**word_data)

    def list(self) -> Iterator[Word]:
        for x in self._session.client.app.words.find(session=self._session):
            yield x
