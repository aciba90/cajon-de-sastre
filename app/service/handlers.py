# pylint: disable=unused-argument
from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING
from app.domain import commands, events, models
from app.domain.models import compute_anagram_hash

if TYPE_CHECKING:
    from app.service.unit_of_work import UnitOfWork


class InvalidSku(Exception):
    pass


def add_word(
    cmd: commands.CreateWord,
    uow: UnitOfWork,
) -> None:
    anagram_hash = compute_anagram_hash(cmd.word)  # TODO move this to domain
    word_model = models.Word(cmd.word, cmd.position, anagram_hash)
    with uow:
        word_dictionary = uow.words.list()
        word_dictionary.add_word(word_model)  # TODO if word exists not add
        uow.words.update(word_dictionary)
        uow.commit()



EVENT_HANDLERS: Dict[Type[events.Event], List[Callable]] = {}

COMMAND_HANDLERS: Dict[Type[commands.Command], Callable] = {
    commands.CreateWord: add_word,
}
