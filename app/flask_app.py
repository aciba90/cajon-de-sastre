from __future__ import annotations

from flask import Flask, jsonify, request
from marshmallow import ValidationError

from app import services, views
from app.core import Word
from app.dependencies import get_repo
from app.schemas import word_schema
from app.services import ExistingWordError, NonExistingWordError

repo = get_repo()

app = Flask(__name__)


@app.route("/words", methods=["POST"])
def add_word():
    """Adds a word."""
    json_data = request.get_json()
    if json_data is None:
        return {"message": "No input data provided"}, 400
    try:
        data = word_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    word = data["word"]
    position = data["position"]
    try:
        services.add_word(word, position, repo)
    except ExistingWordError as e:
        return {"message": str(e)}, 400
    return {"word": word, "position": position}, 201


@app.route("/words/<string:word>", methods=["PATCH"])
def patch_word(word: str):
    """Patches a word."""
    json_data = request.get_json()
    if json_data is None:
        return {"message": "No input data provided"}, 400
    json_data.update({"word": word})
    try:
        data = word_schema.load(json_data)
    except ValidationError as err:
        return err.messages, 422
    word = data["word"]
    position = data["position"]
    try:
        services.update_word(word, position, repo)
    except NonExistingWordError as e:
        return {"message": str(e)}, 400
    return jsonify({"word": word, "position": position}), 200


@app.route("/words/<string:word>", methods=["DELETE"])
def delete_word(word: str):
    """Deletes a word."""
    try:
        services.delete_word(word, repo)
    except NonExistingWordError as e:
        return {"message": str(e)}, 400
    return "Deleted", 204


@app.route("/words", methods=["GET"])
def list_words():
    """Lists existing words ordered by position."""
    word_list = views.list_words(repo.client)
    return jsonify({"data": word_list}), 200


@app.route("/words/<string:word>/anagrams", methods=["GET"])
def get_anagrams(word: str):
    """Returns the anagrams of `word`."""
    anagram_hash = Word(word, -1).anagram_hash
    word_list = views.get_anagrams(anagram_hash, repo.client)
    return jsonify({"data": word_list}), 200
