# -*- coding: utf-8 -*-
import re
import pytest

@pytest.fixture
def urlencode(py2):
    if py2:
        from urllib import urlencode
    else:
        from urllib.parse import urlencode

    return urlencode

@pytest.fixture
def urllib_parse(py2):
    if py2:
        import urlparse as parse
    else:
        from urllib import parse

    return parse

def test_url_encode__mapping(urlencode):
    data = {'key': 'value', 'dt': '2018-03-20T17:00:00+08:00'}

    assert urlencode(data) in [
        # arbitrary order (non-random)
        'dt=2018-03-20T17%3A00%3A00%2B08%3A00&key=value',
        'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    ]

def test_url_decode__dict(urllib_parse):
    query_string = 'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    params = urllib_parse.parse_qs(query_string)

    assert params == {
        'key': ['value'],
        'dt': ['2018-03-20T17:00:00+08:00'] # list of values
    }

def test_url_decode__list(urllib_parse):
    query_string = 'key=value&dt=2018-03-20T17%3A00%3A00%2B08%3A00'
    params = urllib_parse.parse_qsl(query_string)

    assert params == [
        ('key', 'value'),
        ('dt', '2018-03-20T17:00:00+08:00')
    ]

def test_url_encode__unicode__raise_error(urlencode, py2):
    data = {'unicode': u'中文'}

    if py2:
        message = "'ascii' codec can't encode characters in position 0-1:" \
                  " ordinal not in range(128)"
        with pytest.raises(UnicodeEncodeError, match=re.escape(message)) as exc_info:
            urlencode(data)
    else:
        assert urlencode(data) == 'unicode=%E4%B8%AD%E6%96%87'

def test_url_encode__unicode_utf8encode(urlencode):
    data = {'unicode-encoded': u'中文'.encode('utf-8')}
    assert urlencode(data) == 'unicode-encoded=%E4%B8%AD%E6%96%87'

