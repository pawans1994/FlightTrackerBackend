import json
from .ApiUtil import call_get_api

def get_autocomplete_list(url, headers, params):
    autoCompleteparams = {
        'query': params['query'],
        'market': 'US',
        'locale': 'en-US'

    }
    resp = call_get_api(url, autoCompleteparams, headers)
    return resp.json()

def track_one_way(url, headers, params, flight_params = None):
    if flight_params:
        flightParams = flight_params
    else:
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
    print('RR:', resp.json())
    return resp.json()


def extract_flight_data(api_response):
    # resp = json.dumps(api_response)
    itinerary_data = []
    for itinerary in api_response["data"]["itineraries"]:
        outward_leg = []
        return_leg = []
        i = 0
        for leg in itinerary['legs']:
            segment_data = []
            for segment in leg['segments']:
                flight = {
                    'source': segment['origin']['displayCode'],
                    'destination': segment['destination']['displayCode'],
                    'departureTime': segment['departure'],
                    'arrivalTime': segment['arrival'],
                    'price': itinerary['price']['formatted'],
                    'carrierName': segment['operatingCarrier']['name'],
                }
                segment_data.append(flight)
            
            if i == 0:
                outward_leg.extend(segment_data)
                i += 1
            else:
                return_leg.extend(segment_data)
        
        itinerary_data.append({
            'outwardLeg': outward_leg,
            'returnLeg': return_leg
        })
    
    return itinerary_data

def get_celery_worker_status(app):
    i = app.control.inspect()
    availability = i.ping()
    stats = i.stats()
    registered_tasks = i.registered()
    active_tasks = i.active()
    scheduled_tasks = i.scheduled()
    result = {
        'availability': availability,
        'stats': stats,
        'registered_tasks': registered_tasks,
        'active_tasks': active_tasks,
        'scheduled_tasks': scheduled_tasks
    }
    return result