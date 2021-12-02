from app.repositories import Repository
from app.core import compute_anagram_hash


def add_word(word: str, position: int, repo: Repository):
    anagram_hash = get_anagram_hash(word, repo)
    repo.add(word, position, anagram_hash)
    return {"word": word, "position": position}, 201


def update_word(word: str, position: int, repo: Repository):
    repo.update(word, position)
    return word, position


def delete_word(word: str, repo: Repository):
    repo.delete(word)


def get_anagram_hash(word: str, repo: Repository):
    return compute_anagram_hash(word)
