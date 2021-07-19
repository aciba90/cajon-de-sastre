#!/bin/sh
gunicorn --config=python:config app.main:app
