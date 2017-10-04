import json

import requests

url = 'http://127.0.0.1:5000'
event_url = url + '/event'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'API-KEY': 'test'}


def test_sending_without_api_key():
    response = requests.post(url=event_url)
    assert 401 == response.status_code


def test_sending_valid_json_request():
    response = requests.post(url=event_url, data=json.dumps({'name': 'test'}), headers=headers)
    assert 201 == response.status_code
