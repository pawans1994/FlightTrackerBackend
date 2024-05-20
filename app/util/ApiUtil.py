import os
import requests
from dotenv import load_dotenv

def call_get_api(url, params, headers):
    try:
        resp = requests.get(url, params=params, headers=headers)
        return resp
    except:
        print('Exception occurred')
        return {
            'error': 'Error'
        }


def get_flight_url(tripType):
    load_dotenv()
    if (tripType == 'oneway'):
        return os.getenv('ONE_WAY_API')
    else:
        return os.getenv('RETURN_API')

def get_headers():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }

    return headers