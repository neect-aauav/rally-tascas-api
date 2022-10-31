import requests

from celery.utils.log import get_task_logger

from . import db_queue

from neectrally.celery import app

logger = get_task_logger(__name__)
logger.propagate = True

from neectrally.settings import BASE_IRI

AUTH_KEY = '1e7632e81c9122cb00283df1c4f1840f25ecbd6c'

@app.task()
def put_data():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Token {AUTH_KEY}"
    }

    print("Making PATCH")

    print(db_queue.qsize())

    return True