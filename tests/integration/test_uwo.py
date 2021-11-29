# pylint: disable=broad-except
from app.service import unit_of_work
import threading
from app.domain.models import Word, Words
import time
import traceback
from typing import List


def insert_words_dictionary(session, words_dictionary: Words) -> None:
    # TODO test db
    session.client.app.wordsdictionary.update_one(
        {"_id": "0"},
        {"$set": words_dictionary.to_dict()},
        upsert=True,
    )


def get_word_dictionary(session) -> Words:
    word_data = session.client.app.wordsdictionary.find_one({})
    return Words.from_dict(word_data)


def test_uow_can_add_a_word(session_factory):
    session = session_factory()
    words_dictionary = get_word_dictionary(session)
    word = Word("asdf", 0, 12194)
    words_dictionary.add_word(word)

    uow = unit_of_work.MongoUnitOfWork(session_factory)
    with uow:
        uow.words.update(words_dictionary)
        uow.commit()
    words_ = session.client.app.wordsdictionary.find_one({"_id": "0"})
    ww = words_["words"]
    assert ww == [{'word': 'asdf', 'position': 0, 'anagram_hash': 12194}]


def try_to_update_words(words: Words, session_factory, exceptions):
    
    uow = unit_of_work.MongoUnitOfWork(session_factory)
    try:
        with uow:
            uow.words.update(words)
            time.sleep(1)
            uow.commit()
    except Exception as e:
        print(traceback.format_exc())
        exceptions.append(e)


def test_concurrent_updates_to_version_are_not_allowed(session_factory):
    session = session_factory()

    words_dictionary_1 = get_word_dictionary(session)
    words_dictionary_2 = get_word_dictionary(session)
    del session

    words_dictionary_1.add_word(Word("asdf", 0, 12194))
    words_dictionary_2.add_word(Word("asdf1", 1, 12194))

    exceptions: List[Exception] = []

    try_to_allocate_order1 = lambda: try_to_update_words(words_dictionary_1, session_factory, exceptions)
    try_to_allocate_order2 = lambda: try_to_update_words(words_dictionary_2, session_factory, exceptions)
    thread1 = threading.Thread(target=try_to_allocate_order1)
    thread2 = threading.Thread(target=try_to_allocate_order2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    session = session_factory()
    version = session.client.app.wordsdictionary.find_one({})["version"]
    assert version == words_dictionary_2._words.pop().version + 1
    assert len(exceptions) == 1, exceptions
    [exception] = exceptions
    assert "this operation conflicted with another operation." in str(exception)

    words_dictionary = get_word_dictionary(session)
    assert len(words_dictionary._words) == 1
