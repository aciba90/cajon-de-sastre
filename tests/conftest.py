import pytest
import time
import requests
from app import config
from pymongo import MongoClient
from pymongo.client_session import ClientSession
from pymongo.errors import ConnectionFailure


def wait_for_webapp_to_come_up():
    deadline = time.time() + 10
    url = config.get_api_url()
    while time.time() < deadline:
        try:
            return requests.get(url)
        except ConnectionError:
            time.sleep(0.5)
    pytest.fail("API never came up")


def wait_for_mongo_to_come_up(session: ClientSession):
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            return session.client.admin.command("ping")
        except ConnectionFailure:
            time.sleep(0.5)
    pytest.fail("Mongo never came up")


def _get_mongo_session(connection_uri) -> ClientSession:
    return MongoClient(connection_uri).start_session()


@pytest.fixture(scope="function")
def session_factory():
    client = MongoClient(config.get_db_uri())
    client.app.drop_collection("word")
    yield lambda: _get_mongo_session(config.get_db_uri())
    client.app.drop_collection("word")


@pytest.fixture(scope="function")
def mongo_db(session_factory):
    session = session_factory()
    wait_for_mongo_to_come_up(session)
    yield session


@pytest.fixture
def mogo_client():
    from app.dependencies import _client

    yield _client
