from util.TrackUtil import get_autocomplete_list, track_one_way, get_celery_worker_status 
from util.ApiUtil import get_flight_url, get_headers 
from tasks import flask_app, celery_app
from flask import request 
import threading
import os
import signal
import redis
import pickle
import subprocess

beat = None
beat_thread = None
should_run = False
beat_process = None

def start_beat():
    global beat_process
    if beat_process and beat_process.poll() is None:
        print('Beat is already running')
        return
    beat_process = subprocess.Popen(['celery', '-A', 'tasks', 'beat', '--loglevel=info'])
    print('Beat Started')


def stop_beat():
    global beat_process
    if beat_process and beat_process.poll() is None:
        beat_process.terminate()
        beat_process.wait()
        print('Beat Stopped')
    else:
        print('Beat is not running')

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
    global beat_process
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
    threshold = request.args['threshold']
    trip_type = request.args['tripType']
    redis_conn.set('flight_params', pickle.dumps(flightParams))
    redis_conn.set('trip_type', trip_type)
    redis_conn.set('threshold_price', threshold)
    if beat_process and beat_process.poll() is None:
        stop_beat()
    else:
        start_beat()

    return ''

if __name__ == "__main__":
    flask_app.run(debug=True, host="0.0.0.0", port=5000)