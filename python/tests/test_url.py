# -*- coding: utf-8 -*-
import urllib, re
import pytest

def test_url_encode__mapping():
    data = {'key': 'value', 'dt': '2018-03-20T17:00:00+08:00'}

    assert urllib.urlencode(data) in [
        # arbitrary order (non-random)
        'dt=2018-03-20T17%3A00%3A00%2B08%3A00&key=value',
        'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    ]

def test_url_decode__dict():
    import urlparse

    query_string = 'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    params = urlparse.parse_qs(query_string)

    assert params == {
        'key': ['value'],
        'dt': ['2018-03-20T17:00:00+08:00'] # list of values
    }

def test_url_decode__list():
    import urlparse

    query_string = 'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    params = urlparse.parse_qsl(query_string)

    assert params == [
        ('key', 'value'),
        ('dt', '2018-03-20T17:00:00+08:00')
    ]

def test_url_encode__unicode__raise_error():
    data = {'unicode': u'中文'}

    message = "'ascii' codec can't encode characters in position 0-1:" \
              " ordinal not in range(128)"
    with pytest.raises(UnicodeEncodeError, match=re.escape(message)) as exc_info:
        urllib.urlencode(data)

def test_url_encode__unicode_utf8encode():
    data = {'unicode-encoded': u'中文'.encode('utf-8')}
    assert urllib.urlencode(data) == 'unicode-encoded=%E4%B8%AD%E6%96%87'

