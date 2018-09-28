import sys
import requests
import pytest

def test_hello_world():
    query_string = {'greeting': 'Hello, World!'}
    resp = requests.get('http://httpbin/get', params=query_string)
    resp.raise_for_status() # best practice

    assert resp.json()['args']['greeting'] == 'Hello, World!'

def test_http_error__exception_not_raised_immediately():
    resp = requests.get('http://httpbin/status/500')

    # no exception raised
    assert resp.status_code == 500

    # non-200 response may cause subsequent exceptions
    err = [
        'No JSON object could be decoded',
        'Expecting value: line 1 column 1 (char 0)'
    ][int(sys.version_info[0] >= 3)]

    with pytest.raises(ValueError) as excinfo:
        resp.json()
    assert str(excinfo.value) == err
