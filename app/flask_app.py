from __future__ import annotations

from flask import Flask, jsonify, request
from pymongo import MongoClient
from mongoengine import connect
from app import services

from app.config import get_db_uri

app = Flask(__name__)
db_uri = get_db_uri()
client = MongoClient(db_uri)
connect(host=db_uri)

def _init_db():
    lock = client.app.lock.find_one({"_id": 0})
    if lock is None:
        client.app.lock.insert_one({"_id": 0, "version": 0})


_init_db()


@app.route("/words", methods=["POST"])
def add_word():
    word, position = request.json["word"], request.json["position"]
    services.add_word(word, position, client)
    return {"word": word, "position": position}, 201


@app.route("/words/<string:word>", methods=["PATCH"])
def patch_word(word: str):
    position = request.json["position"]
    services.update_word(word, position, client)
    return jsonify({"word": word, "position": position}), 200


@app.route("/words/<string:word>", methods=["DELETE"])
def delete_word(word: str):
    services.delete_word(word, client)
    return "Deleted", 204


@app.route("/words", methods=["GET"])
def list_words():
    word_list = services.list_words(client)
    return jsonify({"data": word_list}), 200


@app.route("/words/<string:word>/anagrams", methods=["GET"])
def get_anagrams(word: str):
    word_list = services.get_anagrams(word, client)
    return jsonify({"data": word_list}), 200
