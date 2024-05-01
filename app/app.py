from util.TrackUtil import get_autocomplete_list, track_one_way
from .tasks import flask_app, celery_app ,long_running_task
from celery.result import AsyncResult#-Line 2
from flask import request 
import redis
import pickle

@flask_app.route('/getAutoCompleteList', methods=['GET'])
def get_auto_complete_list():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete'
    resp = get_autocomplete_list(url ,headers, request.args)
    return resp

@flask_app.route('/flightTrack', methods=['GET'])
def track_flight():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    trip_type = request.args['tripType']
    long_running_task.delay(10)
    if (trip_type == 'oneway'):
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way'
    else:
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip'
        
    resp = track_one_way(url, headers, request.args)
    
    return resp

@flask_app.route('/flightNotification', methods=['GET'])
def get_flight_notification():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    redis_conn = redis.StrictRedis(host='localhost', port=6379,db=0)
    flightParams = {
        'fromId': request.args['sourceId'],
        'toId': request.args['destinationId'],
        'departDate': request.args['departureDate'],
        'returnDate': request.args['returnDate'],
        'adults': '1',
        'currency': 'USD',
        'market': 'US',
        'locale': 'en-US'
    }

    redis_conn.set('flight_params', pickle.dumps(flightParams))
    celery_app.Beat(loglevel='info').run()

    return {
        'error': 'Error'
    }

if __name__ == "__main__":
    flask_app.run(debug=True)