import requests

def test_text_decoding__encoding_in_header(py2):
    resp = requests.get('http://httpbin/encoding/utf8')

    assert resp.headers['content-type'] == 'text/html; charset=utf-8'
    assert resp.encoding == 'utf-8'

    if py2:
        assert type(resp.text) == unicode
        assert type(resp.content) == str
        assert resp.content.decode('utf-8') == resp.text
    else:
        assert type(resp.text) == str
        assert type(resp.content) == bytes
        assert resp.content.decode('utf-8') == resp.text

def test_text_decoding__encoding_in_body__explicitly_provide_encoding_or_guessed_using_chardet(py2):
    resp = requests.get('http://httpbin/xml')

    assert resp.headers['content-type'] == 'application/xml' # no charset

    # http://docs.python-requests.org/en/master/api/#requests.Response.text
    # If Response.encoding is None, encoding will be guessed using chardet.
    assert resp.encoding is None

    if py2:
        assert type(resp.text) == unicode
        assert type(resp.content) == str
    else:
        assert type(resp.text) == str
        assert type(resp.content) == bytes

    assert resp.content.startswith(b"<?xml version='1.0' encoding='us-ascii'?>")
    resp.encoding = 'us-ascii'

    if py2:
        assert type(resp.text) == unicode
        assert type(resp.content) == str
        assert resp.content.decode('us-ascii') == resp.text
    else:
        assert type(resp.text) == str
        assert type(resp.content) == bytes
        assert resp.content.decode('us-ascii') == resp.text
