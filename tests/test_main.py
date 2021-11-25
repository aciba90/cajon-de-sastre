from app.main import Word, WordRepo


def test_0():
    word_repo = WordRepo()
    word = Word(word="car", position=1)
    word_repo.add(word)
