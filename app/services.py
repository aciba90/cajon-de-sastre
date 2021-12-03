from app.core import Word
from app.repositories import Repository


class WordException(Exception):
    """Generic service exception."""


class ExistingWordError(WordException):
    """A word does exist."""


class NonExistingWordError(WordException):
    """A word does not exist."""


def add_word(word: str, position: int, repo: Repository) -> None:
    """Adds a word to the system.

    :param word: Word to add
    :param position: word's position
    :param repo: Repository port
    :raises ExistingWordError: If the word does already exist
    """
    existing_word = repo.get(word)
    if existing_word is not None:
        raise ExistingWordError(f"Word already created: {word}")
    word_ = Word(word, position)
    repo.add(word_)


def update_word(word: str, position: int, repo: Repository) -> None:
    """Updates an existing word in the system.

    :param word: Word to add
    :param position: word's position
    :param repo: Repository port
    :raises NonExistingWordError: If the word does not exist
    """
    existing_word = repo.get(word)
    if existing_word is None:
        raise NonExistingWordError(f"Word does not exist: {word}")
    word_ = Word(word, position)
    repo.update(word_)


def delete_word(word: str, repo: Repository) -> None:
    """Deletes an existing word of the system.

    :param word: Word to add
    :param position: word's position
    :param repo: Repository port
    :raises NonExistingWordError: If the word does not exist
    """
    existing_word = repo.get(word)
    if existing_word is None:
        raise NonExistingWordError(f"Word does not exist: {word}")
    word_ = Word(word, -1)
    repo.delete(word_)
