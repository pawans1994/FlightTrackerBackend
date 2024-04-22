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
