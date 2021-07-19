"""Gunicor configuration"""
import multiprocessing
import os

_timeout = int(os.getenv("APP_TIMEOUT", 30))

# gunicorn config:

bind = "0.0.0.0:80"
workers = int(os.getenv("APP_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
loglevel = os.getenv("LOG_LEVEL", "info")
graceful_timeout = _timeout
timeout = _timeout
