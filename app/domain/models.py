from __future__ import annotations

from typing import Dict, Sequence, Set



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


def compute_anagram_hash(word: str) -> int:
    """[summary]

    Example:
    --------
    >>> compute_anagram_hash("asdf")
    12194
    >>> compute_anagram_hash("fdas")
    12194
    >>> compute_anagram_hash("aas")
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


class Word:
    """
    TODO
    """

    def __init__(self, word: str, position: int, anagram_hash: int):
        self._word=word
        self.position=position
        self.anagram_hash=anagram_hash
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return self._word == other._word

    def __hash__(self) -> int:
        return hash(self._word)

    @property
    def word(self) -> str:
        return self._word

    def to_dict(self) -> Dict:
        return {
            "word": self.word,
            "position": self.position,
            "anagram_hash": self.anagram_hash,
        }
    
    @classmethod
    def from_dict(cls, dict_: Dict) -> Word:
        return cls(
            word=dict_["word"],
            position=dict_["position"],
            anagram_hash=dict_["anagram_hash"],
        )


class Words:
    """
    TODO
    """

    def __init__(self, version: int, words: Sequence[Word]=None):
        self._id = "0"
        self._words: Set[Word] = set(words) if words else set()
        self._version = version

    def add_word(self, word: Word) -> None:
        self._words.add(word)
        # TODO add rules to move positions
    
    def to_dict(self) -> Dict:
        return {
            "_id": self._id, 
            "version": self._version,
            "words": list(map(lambda w: w.to_dict(), self._words)),
        }

    @classmethod
    def from_dict(cls, dict_: Dict) -> Words:
        word_dictionary = cls(
            version=dict_["version"],
            words=list(map(lambda w: Word.from_dict(w), dict_["words"])),
        )
        word_dictionary._id = dict_["_id"]
        return word_dictionary