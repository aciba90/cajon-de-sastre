from pymongo import MongoClient


class Repository:
    def __init__(self, client: MongoClient):
        self.client = client
        self._init_db(self.client)

    @staticmethod
    def _init_db(client):
        lock = client.app.lock.find_one({"_id": 0})
        if lock is None:
            client.app.lock.insert_one({"_id": 0, "version": 0})

    def add(self, word: str, position: int, anagram_hash: int):
        existing_word = self.client.app.word.find_one({"word": word})
        if existing_word is None:
            self.client.app.word.update_many(
                {"position": {"$gte": position}}, {"$inc": {"position": 1}}
            )
            self.client.app.word.insert_one(
                {"word": word, "position": position, "anagram_hash": anagram_hash}
            )

    def update(self, word: str, position: int):
        lock_version = self.client.app.lock.find_one({"_id": 0})
        self.client.app.lock.update_one(
            {"_id": 0, "version": lock_version["version"]},
            {"$inc": {"version": 1}},
        )
        position_old = self.client.app.word.find_one({"word": word})["position"]
        self.client.app.word.update_many(
            {"position": {"$gte": position_old}},
            {"$inc": {"position": 1}},
        )
        self.client.app.word.update_one(
            {"word": word}, {"$set": {"position": position}}
        )

    def delete(self, word: str):
        self.client.app.word.delete_one({"word": word})
