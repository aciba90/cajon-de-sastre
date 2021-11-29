import pymongo


"""
.aggregate([{"$unwind": "$words"}, {"$sort": {"words.position": pymongo.ASCENDING}}, {"$project": {"words.word": True}}] ))

"""

def words(uow):
    projection = {"words.word": True, "words.position": True}
    with uow:
        results = uow.session.client.app.wordsdictionary.find_one(
            {"_id": "0"}, projection=projection, sort=[('words.position', pymongo.ASCENDING)]
        )
        words_ = [w["word"] for w in results["words"]]
        return {"data": words_}


def get_word(word: str, uwo):
    
    return