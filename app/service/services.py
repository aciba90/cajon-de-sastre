from __future__ import annotations

from app.service.unit_of_work import UnitOfWork
from app.domain import models
from app.domain.models import compute_anagram_hash
from typing import List


def is_valid_sku(sku, batches):
    return sku in {b.sku for b in batches}


def patch_word(word: str, position: int, uow: UnitOfWork) -> models.Word:
    with uow:
        return uow.words.get(word)
        # TODO
