from abc import ABC, abstractmethod
from typing import Iterator
from app.domain.models import Word
from dataclasses import asdict


class WordRepo(ABC):
    """TODO"""

    @abstractmethod
    def add(self, word: Word) -> None:
        ...

    @abstractmethod
    def list(self) -> Iterator[Word]:
        ...


class WordMongoRepo(WordRepo):
    def __init__(self, session):
        self._session = session

    def add(self, word: Word) -> None:
        payload = asdict(word)
        _ = self._session.client.app.words.insert_one(payload, session=self._session)

    def list(self) -> Iterator[Word]:
        for x in self._session.client.app.words.find(session=self._session):
            yield x
