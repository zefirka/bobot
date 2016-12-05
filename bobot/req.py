"Requests module"

import requests

def call(url, method='GET', data={}, headers={}, files=None):
    """
        Calls URL:
        @param {str}  url
        @param {str}  [method]
        @param {dict} [data]
        @param {dict} [headers]
        @returns {str}
    """
    if method is 'GET':
        request = requests.get(url, params=data, headers=headers)
    else:
        request = requests.post(url, data=data, headers=headers, files=files)

    request.encoding = 'utf-8'

    return request.text

def get(url, data={}, headers={}):
    "Calls url with method GET"
    return call(url, 'GET', data, headers)

def post(url, data={}, headers={}, files={}):
    "Calls url with method POST"
    return call(url, 'POST', data, headers, files)
