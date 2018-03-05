# -*- coding: utf-8 -*-
import urllib, re
import pytest

def test_urlencode__mapping():
    data = {'key1': '123', 'key2': 'one two three'}

    assert urllib.urlencode(data) in [
        # arbitrary order (non-random)
        'key2=one+two+three&key1=123',
        'key1=123&key2=one+two+three'
    ]

def test_urlencode__unicode__raise_error():
    data = {'unicode': u'中文'}

    message = "'ascii' codec can't encode characters in position 0-1:" \
              " ordinal not in range(128)"
    with pytest.raises(UnicodeEncodeError, match=re.escape(message)) as exc_info:
        urllib.urlencode(data)

def test_urlencode__unicode_utf8encode():
    data = {'unicode-encoded': u'中文'.encode('utf-8')}
    assert urllib.urlencode(data) == 'unicode-encoded=%E4%B8%AD%E6%96%87'

