import threading
from pymongo import MongoClient
from typing import List
import time


def update_word(word: str, position: int, client: MongoClient, exceptions):
    lock_version = client.app.lock.find_one({"_id": 0})
    time.sleep(1)  # Simulate slow function
    try:
        client.app.lock.update_one(
            {"_id": 0, "version": lock_version["version"]},
            {"$inc": {"version": 1}},
            upsert=True,
        )
    except Exception as e:
        exceptions.append(e)
        raise
    position_old = client.app.word.find_one({"word": word})["position"]
    client.app.word.update_many(
        {"position": {"$gte": position_old}},
        {"$inc": {"position": 1}},
    )
    client.app.word.update_one({"word": word}, {"$set": {"position": position}})
    return word, position


def test_concurrent_updates_to_version_are_not_allowed(mogo_client):
    word_1 = ("asdf", 0)
    word_2 = ("fdas", 1)
    mogo_client.app.words.insert_many([{"word": word_1[0], "position": word_1[1]}])
    mogo_client.app.words.insert_many([{"word": word_2[0], "position": word_2[1]}])

    exceptions: List[Exception] = []

    try_to_update_word_2 = lambda: update_word(*word_1, mogo_client, exceptions)
    try_to_update_word_1 = lambda: update_word(*word_1, mogo_client, exceptions)
    thread1 = threading.Thread(target=try_to_update_word_1)
    thread2 = threading.Thread(target=try_to_update_word_2)
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    assert len(exceptions) == 1, exceptions
    [exception] = exceptions
    assert "duplicate key error collection:" in str(exception)
