"""Proyect configuration"""
import os


def get_api_url() -> str:
    """Gets API's url."""
    host = os.environ.get("API_HOST", "api")
    port = 5000
    return f"http://{host}:{port}"


_CONNECTION_URI = (
    "mongodb://mongodb1:27317,mongodb2:27017,mongodb3:27017/app?replicaSet=rsmongo"
)


def get_db_uri() -> str:
    """Gets Mongo's url."""
    return os.environ.get("CONNECTION_URI", _CONNECTION_URI)
