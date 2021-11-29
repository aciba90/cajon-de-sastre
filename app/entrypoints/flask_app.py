from flask import Flask, request, jsonify

from app.service import unit_of_work
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
    cmd = commands.CreateWord(request.json["word"], request.json["position"])
    bus.handle(cmd)
    views.get_word(word, bus.uow)
    return {"word": word_.word, "position": word_.position}


@app.route("/words", methods=["GET"])
def list_words():
    result = views.words(bus.uow)
    return jsonify(result), 200
