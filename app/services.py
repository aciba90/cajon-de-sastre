from app.repositories import Repository
from app.core import Word

class ExistingWordError(Exception):
    pass


class NonExistingWordError(Exception):
    pass


def add_word(word: str, position: int, repo: Repository):
    existing_word = repo.get(word)
    if existing_word is not None:
        raise ExistingWordError(f"Word already created: {word}")
    word_ = Word(word, position)
    repo.add(word_)
    return {"word": word, "position": position}, 201


def update_word(word: str, position: int, repo: Repository):
    existing_word = repo.get(word)
    if existing_word is None:
        raise NonExistingWordError(f"Word does not exist: {word}")
    word_ = Word(word, position)
    repo.update(word_)
    return word, position


def delete_word(word: str, repo: Repository):
    word_ = Word(word, -1)
    repo.delete(word_)
