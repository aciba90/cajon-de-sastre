from unittest.mock import Mock

import inject
import pytest
from app.adapters.repositories import WordRepo


# @pytest.fixture
# def injector() -> None:
#     inject.clear_and_configure(lambda binder: binder.bind(WordRepo, WordRepo()))


# def test_add_word(injector: None):
#     add_word = AddWord()
#     add_word.execute(word="car", position=1)
