from app.service.unit_of_work import DEFAULT_SESSION_FACTORY


session = DEFAULT_SESSION_FACTORY()

def main():
    # session.client.drop_database("app")
    session.start_transaction()
    r = session.client.app.wordsdictionary.update_one(
        {"_id": "0", "version": 2}, {"$set": {"words": [], "version": 3}}, upsert=True
    )
    session.commit_transaction()
    r = session.client.app.wordsdictionary.find_one({"_id": "0"})
    print(r)


if __name__ == "__main__":
    main()
