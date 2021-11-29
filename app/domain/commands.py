# pylint: disable=too-few-public-methods
from dataclasses import dataclass


class Command:
    pass


@dataclass
class CreateWord(Command):
    word: str
    position: int


@dataclass
class UpdateWord(Command):
    word: str
    position: int
