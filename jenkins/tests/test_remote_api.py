import urllib2
import re
import base64
from jenkins.remoteapi import *
import pytest

JENKINS_URL = 'http://localhost:8080'
JENKINS_USER = 'jeremykao'
JENKINS_PASSWD = 'secret'
JENKINS_API_TOKEN = '8c410eb51a7469aa9ddaeb7b5caf3bd0'

def test_csrf_protection_header():
    header = csrf_protection_header(JENKINS_URL, JENKINS_USER, JENKINS_PASSWD)

    assert header[0] == 'Jenkins-Crumb'
    assert re.match(r'[0-9a-f]+', header[1])

def test_remote_scripting__passwd_with_csrf_token__success():
    auth_header = basic_auth_header(JENKINS_USER, JENKINS_PASSWD)
    csrf_header = csrf_protection_header(JENKINS_URL, JENKINS_USER, JENKINS_PASSWD)

    resp = execute_script("println 'Hello, World!'", JENKINS_URL,
        headers=[auth_header, csrf_header])
    assert resp == 'Hello, World!\n'

def test_remote_scripting__passwd_without_csrf_token__403_error():
    auth_header = basic_auth_header(JENKINS_USER, JENKINS_PASSWD)

    with pytest.raises(urllib2.HTTPError) as e:
        execute_script("println 'Hello, World!'", JENKINS_URL, headers=[auth_header])

    assert e.value.code == 403
    assert e.value.reason == 'No valid crumb was included in the request'

def test_remote_scripting__api_token_without_csrf_token__success():
    auth_header = basic_auth_header(JENKINS_USER, JENKINS_API_TOKEN)

    # unexpected success? https://jenkins.io/changelog/#v2.96
    # Do not require CSRF crumb to be provided when the request is authenticated using API token.
    resp = execute_script("println 'Hello, World!'", JENKINS_URL, headers=[auth_header])
    assert resp == 'Hello, World!\n'

