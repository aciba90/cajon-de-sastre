FROM python:3.9-slim-bullseye

# RUN apt-get update && apt-get install make 
COPY requirements.txt /tmp/requirements.txt
RUN pip install -U pip wheel -r /tmp/requirements.txt

COPY . /code
WORKDIR /code
