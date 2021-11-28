from __future__ import annotations

import abc
from typing import Callable

from app.adapters import repositories
from app.adapters.repositories import WordMongoRepo
from pymongo.client_session import ClientSession
from pymongo import MongoClient
from app.config import get_db_uri


class UnitOfWork(abc.ABC):
    words: repositories.WordRepo

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(self, *args):
        # self.rollback()
        ...

    @abc.abstractmethod
    def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    def rollback(self):
        raise NotImplementedError


_CONNECTION_URI = get_db_uri()


def get_mongo_session(connection_uri: str = _CONNECTION_URI) -> ClientSession:
    return MongoClient(connection_uri).start_session()


DEFAULT_SESSION_FACTORY = get_mongo_session


class MongoUnitOfWork(UnitOfWork):
    def __init__(
        self, session_factory: Callable[..., ClientSession] = DEFAULT_SESSION_FACTORY
    ):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.session.start_transaction()
        self.words = WordMongoRepo(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        # super().__exit__(*args)
        self.session.end_session()

    def commit(self):
        # raise Exception("asd")
        self.session.commit_transaction()

    def rollback(self):
        self.session.abort_transaction()
