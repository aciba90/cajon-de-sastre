from __future__ import annotations

from app.service.unit_of_work import UnitOfWork
from app.domain import models
from app.domain.models import compute_anagram_hash
from typing import List


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_word(
    word: str,
    position: int,
    uow: UnitOfWork,
) -> None:
    anagram_hash = compute_anagram_hash(word)
    word_model = models.Word(word, position, anagram_hash)
    with uow:
        uow.words.add(word_model)
        uow.commit()


def get_word(word: str, uow: UnitOfWork) -> models.Word:
    with uow:
        return uow.words.get(word)


def patch_word(word: str, position: int, uow: UnitOfWork) -> models.Word:
    with uow:
        return uow.words.get(word)
        # TODO


def get_words(uow: UnitOfWork) -> List[models.Word]:
    with uow:
        words = uow.words.list()
    return list(words)
