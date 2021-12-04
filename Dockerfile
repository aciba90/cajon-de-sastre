FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get install make 
COPY requirements.txt requirements-dev.txt /tmp/
RUN pip install -U pip wheel -r /tmp/requirements.txt -r /tmp/requirements-dev.txt

COPY . /code
WORKDIR /code

ENV FLASK_APP "app/flask_app"
CMD python -m flask run
