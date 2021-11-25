"""TODO"""

from dataclasses import dataclass
from functools import cached_property
from typing import Dict, Iterator, Set

_lookup: Dict[str, int] = {
    "A": 2,
    "a": 2,
    "B": 3,
    "b": 3,
    "C": 5,
    "c": 5,
    "D": 7,
    "d": 7,
    "E": 11,
    "e": 11,
    "F": 13,
    "f": 13,
    "G": 17,
    "g": 17,
    "H": 19,
    "h": 19,
    "I": 23,
    "i": 23,
    "J": 29,
    "j": 29,
    "K": 31,
    "k": 31,
    "L": 37,
    "l": 37,
    "M": 41,
    "m": 41,
    "N": 43,
    "n": 43,
    "O": 47,
    "o": 47,
    "P": 53,
    "p": 53,
    "Q": 59,
    "q": 59,
    "R": 61,
    "r": 61,
    "S": 67,
    "s": 67,
    "T": 71,
    "t": 71,
    "U": 73,
    "u": 73,
    "V": 79,
    "v": 79,
    "W": 83,
    "w": 83,
    "X": 89,
    "x": 89,
    "Y": 97,
    "y": 97,
    "Z": 101,
    "z": 101,
}


def _compute_anagram_hash(word: str) -> int:
    """[summary]

    Example:
    --------
    >>> _compute_anagram_hash("asdf")
    12194
    >>> _compute_anagram_hash("fdas")
    12194
    >>> _compute_anagram_hash("aas")
    268

    :param word: [description]
    :type word: str
    :return: [description]
    :rtype: int
    """
    anagram_hash = 1
    for letter in word:
        anagram_hash *= _lookup.get(letter, 1)
    return anagram_hash


@dataclass(frozen=True)
class Word:
    """
    TODO
    """

    word: str
    position: int

    @cached_property
    def anagram_hash(self) -> int:
        """Computed anagram hash property.

        :return: Anagram hash.
        """
        return _compute_anagram_hash(self.word)


class WordRepo:
    """TODO"""

    def __init__(self):
        self._data: Set[Word] = set()

    def add(self, word: Word):
        """[summary]

        :param word: [description]
        :type word: Word
        """
        self._data.add(word)

    def get_all(self) -> Iterator[Word]:
        """[summary]

        :yield: [description]
        :rtype: Iterator[Word]
        """
        for word in self._data:
            yield word
