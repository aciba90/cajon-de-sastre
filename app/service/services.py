from __future__ import annotations

from app.service import unit_of_work
from app.domain import models
from app.domain.models import compute_anagram_hash
from typing import List


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def add_word(
    word: str, position: str, uow: unit_of_work.AbstractUnitOfWork,
) -> None:
    anagram_hash = compute_anagram_hash(word)
    word_model = models.Word(word, position, anagram_hash)
    with uow:
        uow.words.add(word_model)
        uow.commit()


def get_words(uow: unit_of_work.AbstractUnitOfWork) -> List[models.Word]:
    with uow:
        words = uow.words.list()
    return words
