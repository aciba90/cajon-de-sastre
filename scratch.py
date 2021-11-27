import pymongo
from pymongo import MongoClient
from app.adapters.repositories import WordRepo
from app.domain.models import Word
from typing import Iterator
from dataclasses import asdict
from app.service import unit_of_work

CONNECTION_URI = "mongodb://root:example@localhost:27017/"


DEFAULT_SESSION_FACTORY = lambda: MongoClient(CONNECTION_URI).start_session()
client = DEFAULT_SESSION_FACTORY()
# db = client.get_database("words")
# print(db)

# category_index = collection_name.create_index("category")

class WordMongoRepo(WordRepo):

    def __init__(self, session):
        self._session = session
    
    def add(self, word: Word) -> None:
        payload = asdict(word)
        result = self._session.client.app.words.insert_one(payload)

    def list(self) -> Iterator[Word]:
        for x in self._words_collection.find():
            yield x


class MongoUnitOfWork(unit_of_work.UnitOfWork):

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()
        self.words = WordMongoRepo(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()


with MongoUnitOfWork() as uow:
    word = Word("asdfa", 0, 123)
    uow.words.add(word)
    words = uow.words.list()
    print(list(words))
