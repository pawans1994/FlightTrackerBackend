from .ApiUtil import call_get_api

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


def extract_flight_data(api_response):
    itinerary_data = []
    for itinerary in api_response['itineraries']:
        outward_leg = []
        return_leg = []
        for i, leg in enumerate(itinerary['legs']):
            segment_data = []
            for segment in leg['segments']:
                flight = {
                    'source': segment['origin']['displayCode'],
                    'destination': segment['destination']['displayCode'],
                    'departureTime': segment['departure'],
                    'arrivalTime': segment['arrival'],
                    'price': itinerary['price']['formatted'],
                    'carrierName': segment['operatingCarrier']['name']
                }
                segment_data.append(flight)
            if i == 0:
                outward_leg.extend(segment_data)
            else:
                return_leg.extend(segment_data)
            print(outward_leg, return_leg)

        itinerary_data.append({
            'outwardLeg': outward_leg[:],
            'returnLeg': return_leg[:]
        })
        outward_leg = []
        return_leg = []

    return itinerary_data