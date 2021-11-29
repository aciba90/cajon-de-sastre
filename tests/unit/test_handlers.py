# pylint: disable=no-self-use
from __future__ import annotations

from collections import defaultdict
from datetime import date
from typing import Dict, List

import pytest
from app import bootstrap
from app.adapters import repositories
from app.domain import commands
from app.domain.models import Words
from app.service import unit_of_work


class FakeRepository(repositories.Repository):
    def __init__(self, words=None):
        self._words = words or Words()

    def update(self, word_dictionary: Words):
        self._words = word_dictionary

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


def bootstrap_test_app():
    return bootstrap.bootstrap(
        uow=FakeUnitOfWork(),
        publish=lambda *args: None,
    )


class TestAddWord:
    def test_add_new_word(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateWord("asdf", 0))
        assert bus.uow.committed


# @pytest.mark.xfail
# def test_get_word():
#     uow = FakeUnitOfWork()
#     services.add_word("asdf", 0, uow)
#     word = services.get_word("asdf", uow)
#     assert word.word == "asdf"
#     assert word.position == 0
#     assert word.anagram_hash == 12194


# @pytest.mark.xfail
# def test_get_words_in_correct_order():
#     uow = FakeUnitOfWork()
#     services.add_word("word1", 1, uow)
#     services.add_word("word0", 0, uow)
#     words = services.get_words(uow)
#     assert words[0].word == "word0"
#     assert words[0].position == 0
#     assert words[1].word == "word1"
#     assert words[1].position == 1
