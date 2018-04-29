import urllib, urllib2
import mimetools
import json
import pytest

def test_urlopen__return_file_like():
    resp = urllib2.urlopen('https://httpbin.org/response-headers?myheader=myvalue')

    assert resp.geturl() == 'https://httpbin.org/response-headers?myheader=myvalue'
    assert resp.getcode() == 200

    # meta-information
    info = resp.info()
    assert isinstance(info, mimetools.Message)
    assert info.getheader('myheader') == 'myvalue'

    # file-like
    assert json.loads(resp.read()) == {
        'Content-Type': 'application/json',
        'myheader': 'myvalue'
    }

def test_urlopen__non_200_response__http_error():
    with pytest.raises(urllib2.HTTPError) as e:
        urllib2.urlopen('https://httpbin.org/status/500')

    assert e.value.code == 500
    assert e.value.reason == 'INTERNAL SERVER ERROR'

def test_urlopen__invalid_host__url_error():
    with pytest.raises(urllib2.URLError) as e:
        urllib2.urlopen('https://httpbin/invalid-host')

    # https://docs.python.org/2/library/socket.html#socket.gaierror
    cause = e.value.reason
    assert cause.args == (8, 'nodename nor servname provided, or not known')

def test_urlopen__redirection():
    resp = urllib2.urlopen('https://httpbin.org/redirect-to?' + urllib.urlencode({
        'url': 'https://www.python.org/'
    }))

    assert resp.geturl() == 'https://www.python.org/'

def test_basic_auth__no_handler__401_error():
    with pytest.raises(urllib2.HTTPError) as e:
        urllib2.urlopen('https://httpbin.org/basic-auth/user/passwd')

    assert e.value.code == 401

def test_basic_auth__custom_opener_with_handler__authenticated():
    auth_url = 'https://httpbin.org/basic-auth/user/passwd' # Www-Authenticate: Basic realm="Fake Realm"

    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password(realm='Fake Realm', uri=auth_url, user='user', passwd='passwd')
    opener = urllib2.build_opener(auth_handler)

    resp = opener.open('https://httpbin.org/basic-auth/user/passwd')
    assert json.loads(resp.read()) == {
        'authenticated': True,
        'user': 'user'
    }

