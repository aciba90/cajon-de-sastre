import pymongo


def words(uow):
    projection = {"_id": False, "words": True}
    with uow:
        results = uow.session.client.app.wordsdictionary.find_one(
            {"_id": "0"}, projection=projection, sort=[('position', pymongo.ASCENDING)]
        )
        return {"data": results["words"]}
