import urllib, urllib2
import base64
import re

def basic_auth_header(user, api_token):
    credential = base64.b64encode('%s:%s' % (user, api_token))
    return 'Authorization', 'Basic %s' % credential

def csrf_protection_header(jenkins_url, user, api_token):
    url = jenkins_url + '/crumbIssuer/api/xml?xpath=concat(//crumbRequestField,":",//crumb)'

    request = urllib2.Request(url)
    request.add_header(*basic_auth_header(user, api_token))

    resp = urllib2.urlopen(request).read()
    match = re.match(r'(?P<header>[^:]+):(?P<value>.+)', resp) # e.g. 'Jenkins-Crumb:abc123def'
    assert match, resp

    return match.group('header'), match.group('value')

def execute_script(groovy_script, jenkins_url, headers=[]):
    data = urllib.urlencode({'script': groovy_script})
    request = urllib2.Request(jenkins_url + '/scriptText', data)

    for header in headers:
        request.add_header(*header)
    return urllib2.urlopen(request).read()
