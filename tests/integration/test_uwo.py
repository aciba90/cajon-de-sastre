# pylint: disable=broad-except
from app.service import unit_of_work



def insert_word(session, word: str, position: int, anagram_hash: int) -> None:
    session.client.test.words.insert_one({
            "word": word,
            "position": position,
            "anagram_hash": anagram_hash,
        }
    )


def test_uow_can_retrieve_a_batch_and_allocate_to_it(session_factory):
    session = session_factory()
    insert_word(session, "asdf", 0, 12194)

    uow = unit_of_work.MongoUnitOfWork(session_factory)
    with uow:
        word = uow.words.get(word="asdf")
        uow.commit()

    assert word.word == "asdf"
    assert word.position == 0
    assert word.anagram_hash == 12194
