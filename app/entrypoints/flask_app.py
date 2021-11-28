from flask import Flask, request

from app.service import services, unit_of_work
from app.service.unit_of_work import DEFAULT_SESSION_FACTORY
import pymongo

app = Flask(__name__)


@app.route("/words", methods=["POST"])
def add_word():
    services.add_word(
        request.json["word"],
        request.json["position"],
        unit_of_work.MongoUnitOfWork(),
    )
    return "OK", 201


@app.route("/words/<string:word>", methods=["PATCH"])
def patch_word(word: str):
    word = services.patch_word(
        word,
        request.json["position"],
        unit_of_work.MongoUnitOfWork(),
    )
    return {"word": word.word, "position": word.position}


session = DEFAULT_SESSION_FACTORY()

@app.route("/words", methods=["GET"])
def list_words():
    projection = {"_id": False, "word": True}
    results = session.client.app.words.find(
        {}, projection=projection, sort=[('position', pymongo.ASCENDING)]
    )
    words = list(map(lambda r: r["word"], results))
    return {"data": words}
