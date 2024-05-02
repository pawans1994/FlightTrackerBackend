from util.TrackUtil import get_autocomplete_list, track_one_way  
from util.ApiUtil import get_flight_url, get_headers 
from tasks import flask_app, celery_app
from flask import request 
import redis
import pickle

@flask_app.route('/getAutoCompleteList', methods=['GET'])
def get_auto_complete_list():
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete'
    resp = get_autocomplete_list(url ,get_headers(), request.args)
    return resp

@flask_app.route('/flightTrack', methods=['GET'])
def track_flight():
    
    trip_type = request.args['tripType']
    
    url = get_flight_url(trip_type)
        
    resp = track_one_way(url, get_headers(), request.args)
    
    return resp

@flask_app.route('/flightNotification', methods=['GET'])
def get_flight_notification():

    redis_conn = redis.StrictRedis(host='redis', port=6379,db=0)
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
    trip_type = request.args['tripType']
    # trip_type = request.args['threshold_price']

    redis_conn.set('flight_params', pickle.dumps(flightParams))
    redis_conn.set('trip_type', trip_type)
    redis_conn.set('threshold_price', '200')
    celery_app.Beat(loglevel='info').run()

    return 200, ''

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=5000)