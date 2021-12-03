"""Core module.

In order to distinguise anagrams, let's introduce our approach.

Theorem: The Fundamental Theorem of Arithmetic
Every positive integer different from 1 can be written uniquely as a product of 
primes.

The strategy is to assing a prime number to each char of our alphabet and given a
word multiply those numbers. 
That would be a unique representation (hash) of the set of anagrams of the given word as:
    1. Previous theorem.
    2. As the product of numbers is commutative two words that are anagrams of each other 
    would have the same product of primes.
"""

from typing import Dict
from functools import lru_cache, cached_property

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


@lru_cache(maxsize=int(1e3))
def _compute_anagram_hash(word: str) -> int:
    """Computes an anagram hash associated to `word`

    If n := len(word) and k := lenght of our alphabet then:
    Time complexity: Average O(n), Worst: O(nlogn)
    Space complexity: O(1)

    Example:
    --------
    >>> _compute_anagram_hash("asdf")
    12194
    >>> _compute_anagram_hash("fdas")
    12194
    >>> _compute_anagram_hash("aas")
    268

    :param word: Word ot compute its anagram hash.
    :return: anagram hash of `word`
    """
    anagram_hash = 1
    for letter in word:
        anagram_hash *= _lookup.get(letter, 1)
    return anagram_hash


class Word:
    """Word domain model"""

    def __init__(self, word: str, position: int = -1):
        self._word = word
        self.position = position

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Word):
            return False
        return self._word == other._word

    def __hash__(self) -> int:
        return hash(self._word)

    @cached_property
    def word(self) -> str:
        return self._word

    @cached_property
    def anagram_hash(self) -> int:
        return _compute_anagram_hash(self._word)
