from pymongo import MongoClient
from app.services import Repository

from app.config import get_db_uri

_client = MongoClient(get_db_uri())


def get_repo(client: MongoClient = _client) -> Repository:
    return Repository(client)
