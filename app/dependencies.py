from pymongo import MongoClient

from app.config import get_db_uri
from app.repositories import MongoRepository, Repository

_client = MongoClient(get_db_uri())


def get_repo(client: MongoClient = _client) -> Repository:
    """Repository factory."""
    return MongoRepository(client)
