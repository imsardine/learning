import requests
from collections import OrderedDict

def test_query_string__none_values_excluded():
    params = OrderedDict([ # to simplify assertion
        ('key', 'value'),
        ('key-list', ['value1', 'value2']),
        ('key-none', None),
    ])

    resp = requests.get('http://httpbin/get', params=params)
    assert resp.url == 'http://httpbin/get?key=value&key-list=value1&key-list=value2'
    assert 'key-none' not in resp.url
