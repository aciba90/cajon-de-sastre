from flask import Flask, request, jsonify

from app.service import services, unit_of_work
from app.service.unit_of_work import DEFAULT_SESSION_FACTORY
import pymongo
from app import bootstrap, views
from app.domain import commands

app = Flask(__name__)
bus = bootstrap.bootstrap()


@app.route("/words", methods=["POST"])
def add_word():
    cmd = commands.CreateWord(request.json["word"], request.json["position"])
    bus.handle(cmd)
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
    result = views.words(bus.uow)
    return jsonify(result), 200
