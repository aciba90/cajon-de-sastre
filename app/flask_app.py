from __future__ import annotations

from typing import Dict

import pymongo
from flask import Flask, jsonify, request
from pymongo import MongoClient
from mongoengine import connect, Document, StringField, IntField

from app.config import get_db_uri

app = Flask(__name__)
db_uri = get_db_uri()
client = MongoClient(db_uri)
connect(host=db_uri)


class Word(Document):
    word = StringField(required=True)
    position = IntField(required=True)
    anagram_hash = IntField(required=True)


_lookup: Dict[str, int] = {
    "A": 2,
    "a": 2,
    "B": 3,
    "b": 3,
    "C": 5,
    "c": 5,
    "D": 7,
    "d": 7,
    "E": 11,
    "e": 11,
    "F": 13,
    "f": 13,
    "G": 17,
    "g": 17,
    "H": 19,
    "h": 19,
    "I": 23,
    "i": 23,
    "J": 29,
    "j": 29,
    "K": 31,
    "k": 31,
    "L": 37,
    "l": 37,
    "M": 41,
    "m": 41,
    "N": 43,
    "n": 43,
    "O": 47,
    "o": 47,
    "P": 53,
    "p": 53,
    "Q": 59,
    "q": 59,
    "R": 61,
    "r": 61,
    "S": 67,
    "s": 67,
    "T": 71,
    "t": 71,
    "U": 73,
    "u": 73,
    "V": 79,
    "v": 79,
    "W": 83,
    "w": 83,
    "X": 89,
    "x": 89,
    "Y": 97,
    "y": 97,
    "Z": 101,
    "z": 101,
}


def compute_anagram_hash(word: str) -> int:
    """[summary]

    Example:
    --------
    >>> compute_anagram_hash("asdf")
    12194
    >>> compute_anagram_hash("fdas")
    12194
    >>> compute_anagram_hash("aas")
    268

    :param word: [description]
    :type word: str
    :return: [description]
    :rtype: int
    """
    anagram_hash = 1
    for letter in word:
        anagram_hash *= _lookup.get(letter, 1)
    return anagram_hash


@app.route("/words", methods=["POST"])
def add_word():
    word, position = request.json["word"], request.json["position"]
    anagram_hash = compute_anagram_hash(word)
    Word.objects(position__gte=position).update(inc__position=1)
    if Word.objects(word=word).first() is None:
        word_db = Word(word=word, position=position, anagram_hash=anagram_hash)
        word_db.save()
    return {"word": word, "position": position}, 201


@app.route("/words/<string:word>", methods=["PATCH"])
def patch_word(word: str):
    position = request.json["position"]
    position_old = Word.objects(word=word).first().position
    Word.objects(position__gte=position_old).update(inc__position=1)
    Word.objects(word=word).update_one(position=position)
    return jsonify({"word": word, "position": position}), 200


@app.route("/words/<string:word>", methods=["DELETE"])
def delete_word(word: str):
    Word.objects(word=word).delete()
    return "Deleted", 204


@app.route("/words", methods=["GET"])
def list_words():
    # TODO Change to mongoengine
    result = list(
        client.app.word.find(
            {},
            projection={"_id": False, "word": True},
            sort=[("position", pymongo.ASCENDING)],
        )
    )
    result = {"data": list(map(lambda w: w["word"], result))}
    return jsonify(result), 200


@app.route("/words/<string:word>/anagrams", methods=["GET"])
def get_anagrams(word: str):
    anagram_hash = compute_anagram_hash(word)
    result = list(
        Word.objects(anagram_hash=anagram_hash).fields(word=True)  # TODO sort
    )
    result_ = {"data": list(map(lambda w: w["word"], result))}
    return jsonify(result_), 200
