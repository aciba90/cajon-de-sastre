from app.adapters import repositories
from app.service import services, unit_of_work
from app.domain.models import Word, Words

import pytest


class FakeRepository(repositories.Repository):
    def __init__(self, words=None):
        self._words = words or Words(version=1)

    def update(self, word_dictionary: Words):
        self._words = word_dictionary

    def get(self, word: str) -> Word:
        # return next(w for w in self._words if w.word == word)
        ...

    def list(self):
        return self._words


class FakeUnitOfWork(unit_of_work.UnitOfWork):
    def __init__(self):
        self.words = FakeRepository()
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_word():
    uow = FakeUnitOfWork()
    services.add_word("asdf", 0, uow)
    assert uow.committed


@pytest.mark.xfail
def test_get_word():
    uow = FakeUnitOfWork()
    services.add_word("asdf", 0, uow)
    word = services.get_word("asdf", uow)
    assert word.word == "asdf"
    assert word.position == 0
    assert word.anagram_hash == 12194


@pytest.mark.xfail
def test_get_words_in_correct_order():
    uow = FakeUnitOfWork()
    services.add_word("word1", 1, uow)
    services.add_word("word0", 0, uow)
    words = services.get_words(uow)
    assert words[0].word == "word0"
    assert words[0].position == 0
    assert words[1].word == "word1"
    assert words[1].position == 1
