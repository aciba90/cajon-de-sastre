import logging

from fastapi.logger import logger

from app.config import LOG_LEVEL

# Set logger, taken from:
# https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker/issues/19

gunicorn_logger = logging.getLogger("gunicorn.error")
logger.handlers = gunicorn_logger.handlers
if __name__ != "main":
    logger.setLevel(gunicorn_logger.level)
else:
    logger.setLevel(LOG_LEVEL)
