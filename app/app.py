from flask import Flask, request
from flask_cors import CORS
from util.ApiUtil import call_get_api
from util.TrackUtil import get_autocomplete_list, track_one_way

app = Flask(__name__)
CORS(app)

@app.route('/getAutoCompleteList', methods=['GET'])
def get_auto_complete_list():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/auto-complete'
    resp = get_autocomplete_list(url ,headers, request.args)
    return resp



@app.route('/flightTrack', methods=['GET'])
def track_flight():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }
    trip_type = request.args['tripType']
    if (trip_type == 'oneway'):
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way'
    else:
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip'
    
    resp = track_one_way(url, headers, request.args)
    
    return resp

if __name__ == '__main__':
   app.run(port=5000)

