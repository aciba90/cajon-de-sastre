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
        self._words = words or Words(version=1)

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
    def test_for_new_product(self):
        bus = bootstrap_test_app()
        bus.handle(commands.CreateWord("asdf", 0))
        assert bus.uow.committed
