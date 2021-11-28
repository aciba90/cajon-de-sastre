from app.adapters import repositories
from app.service import services, unit_of_work


class FakeRepository(repositories.WordRepo):
    def __init__(self, words):
        self._words = list(words)

    def add(self, word):
        self._words.append(word)

    def list(self):
        return list(self._words)


class FakeUnitOfWork(unit_of_work.UnitOfWork):
    def __init__(self):
        self.words = FakeRepository([])
        self.committed = False

    def commit(self):
        self.committed = True

    def rollback(self):
        pass


def test_add_word():
    uow = FakeUnitOfWork()
    services.add_word("asdf", 0, uow)
    assert uow.committed
    words = services.get_words(uow)
    assert words[0].word == "asdf"
    assert words[0].position == 0
    assert words[0].anagram_hash == 12194


def test_get_words_in_correct_order():
    uow = FakeUnitOfWork()
    services.add_word("word1", 1, uow)
    services.add_word("word0", 0, uow)
    words = services.get_words(uow)
    assert words[0].word == "word0"
    assert words[0].position == 0
    assert words[1].word == "word1"
    assert words[1].position == 1
