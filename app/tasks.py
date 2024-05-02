from config import create_app
from celery import shared_task 
from util.TrackUtil import track_one_way
from util.ApiUtil import get_flight_url, get_headers
import redis
import pickle

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

@shared_task
def getResults() -> int:
    redis_conn = redis.StrictRedis(host='localhost', port=6379,db=0)
    flight_details = redis_conn.get('flight_params')
    trip_type = redis_conn.get('trip_type')
    result = pickle.loads(flight_details)
    resp = track_one_way(get_flight_url(trip_type), get_headers(), result)


    
