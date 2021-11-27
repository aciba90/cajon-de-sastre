from __future__ import annotations
import abc
from app.adapters import repositories


class UnitOfWork(abc.ABC):
    words: repositories.WordRepo

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        self.rollback()

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError
