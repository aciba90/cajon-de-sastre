from __future__ import annotations

from flask import Flask, jsonify, request
from app import services, views
from app.services import ExistingWordError, NonExistingWordError

from app.dependencies import get_repo
from app.core import Word


repo = get_repo()

app = Flask(__name__)


@app.route("/words", methods=["POST"])
def add_word():
    word = request.json["word"]
    position = request.json["position"]
    try:
        services.add_word(word, position, repo)
    except ExistingWordError as e:
        return {"message": str(e)}, 400
    return {"word": word, "position": position}, 201


@app.route("/words/<string:word>", methods=["PATCH"])
def patch_word(word: str):
    position = request.json["position"]
    try:
        services.update_word(word, position, repo)
    except NonExistingWordError as e:
        return {"message": str(e)}, 400
    return jsonify({"word": word, "position": position}), 200


@app.route("/words/<string:word>", methods=["DELETE"])
def delete_word(word: str):
    services.delete_word(word, repo)
    return "Deleted", 204


@app.route("/words", methods=["GET"])
def list_words():
    word_list = views.list_words(repo.client)
    return jsonify({"data": word_list}), 200


@app.route("/words/<string:word>/anagrams", methods=["GET"])
def get_anagrams(word: str):
    anagram_hash = Word(word, -1).anagram_hash
    word_list = views.get_anagrams(anagram_hash, repo.client)
    return jsonify({"data": word_list}), 200
