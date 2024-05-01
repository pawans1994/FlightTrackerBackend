from .config import create_app #-Line 1
from celery import shared_task 
from time import sleep
from celery.result import AsyncResult
import redis
import pickle

flask_app = create_app()  #-Line 2
celery_app = flask_app.extensions["celery"]
 #-Line 3

@shared_task(ignore_result=False) #-Line 4
def long_running_task(iterations) -> int:#-Line 5
    result = 0
    for i in range(iterations):
        result += i
        sleep(2)
    redis_conn = redis.StrictRedis(host='localhost', port=6379,db=0)
    redis_conn.set('result_id', result)

@shared_task
def getResults() -> int:
    redis_conn = redis.StrictRedis(host='localhost', port=6379,db=0)
    flight_details = redis_conn.get('flight_params')
    result = pickle.loads(flight_details)
    print('Ready', result)
