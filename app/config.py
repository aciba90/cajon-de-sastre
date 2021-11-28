import os


def get_api_url() -> str:
    host = os.environ.get("API_HOST", "api")
    port = 5000
    return f"http://{host}:{port}"


_CONNECTION_URI = (
    "mongodb://mongodb1:27317,mongodb2:27017,mongodb3:27017/?replicaSet=rsmongo"
)


def get_db_uri() -> str:
    # TODO get from env
    return _CONNECTION_URI
