import requests

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
    url = ''
    if (tripType == 'oneway'):
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-one-way'
    else:
        url = 'https://skyscanner80.p.rapidapi.com/api/v1/flights/search-roundtrip'
    
    return url

def get_headers():
    headers = {
        'X-RapidAPI-Key': '159f65f07emsh451ea3d1ef23233p1a1b7ajsn5ee0e6b24b3b',
        'X-RapidAPI-Host': 'skyscanner80.p.rapidapi.com'
    }

    return headers