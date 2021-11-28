from flask import Flask, request

from app.service import services, unit_of_work

app = Flask(__name__)


@app.route("/words", methods=["POST"])
def add_word():
    services.add_word(
        request.json["word"],
        request.json["position"],
        unit_of_work.MongoUnitOfWork(),
    )
    return "OK", 201
