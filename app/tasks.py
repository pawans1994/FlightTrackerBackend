from config import create_app
from celery import shared_task 
from util.TrackUtil import track_one_way, extract_flight_data
from util.ApiUtil import get_flight_url, get_headers
from util.EmailUtil import send_mail
import redis
import pickle

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

@shared_task(name='app.tasks.getResults')
def getResults() -> int:
    redis_conn = redis.StrictRedis(host='redis', port=6379,db=0)
    fromID = '#SENDER Email Id'
    toIds = ['#Receiver Email Id']
    flight_details = redis_conn.get('flight_params')
    trip_type =redis_conn.get('trip_type').decode('utf-8')
    result = pickle.loads(flight_details)
    flightParams = {
            'fromId': result['fromId'],
            'toId': result['toId'],
            'departDate': result['departDate'],
            'adults': '1',
            'currency': 'USD',
            'market': 'US',
            'locale': 'en-US'
    }
    if (trip_type == 'roundtrip'):
        flightParams['returnDate'] = result['returnDate']
    url = get_flight_url(trip_type)
    threshold = redis_conn.get('threshold_price').decode('utf-8')
    resp = track_one_way(url, get_headers(), result, flight_params=flightParams)
    response = extract_flight_data(resp)
    for r in response:
        price = r['outwardLeg'][0]['price'][1:]
        print(price, threshold)
        if int(price) <= int(threshold):
            send_mail(fromID, toIds, 'Flight Price below threshold', str(r))
            print('Email sent')



    
