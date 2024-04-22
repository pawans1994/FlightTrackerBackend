from util.ApiUtil import call_get_api

def get_autocomplete_list(url, headers, params):
    autoCompleteparams = {
        'query': params['query'],
        'market': 'US',
        'locale': 'en-US'

    }
    resp = call_get_api(url, autoCompleteparams, headers)
    return resp.json()

def track_one_way(url, headers, params):
    flightParams = {
        'fromId': params['sourceId'],
        'toId': params['destinationId'],
        'departDate': params['departureDate'],
        'returnDate': params['returnDate'],
        'adults': '1',
        'currency': 'USD',
        'market': 'US',
        'locale': 'en-US'
    }
    resp = call_get_api(url, flightParams, headers)
    return resp.json()