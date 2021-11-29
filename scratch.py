from app.config import get_db_uri
import pymongo

URI = get_db_uri()
client = pymongo.MongoClient(URI)
