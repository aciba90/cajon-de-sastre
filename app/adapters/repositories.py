from abc import ABC, abstractmethod
from typing import Dict, Iterator, List
from app.domain.models import Word


class WordRepo(ABC):
    """TODO"""

    @abstractmethod
    def add(self, word: Word) -> None:
        ...

    @abstractmethod
    def list(self) -> Iterator[Word]:
        ...


class WordFakeRepo(WordRepo):
    """TODO"""

    def __init__(self):
        self._data: List[Word] = []

    def add(self, word: Word):
        """[summary]

        :param word: [description]
        :type word: Word
        """
        self._data.append(word.to_dict())

    def get_all(self) -> Iterator[Word]:
        """[summary]

        :yield: [description]
        :rtype: Iterator[Word]
        """
        for word in self._data:
            yield word