import pytest
import requests
import time
import logging

def hockeyapp_get(entrypoint, config, params={}):
    headers = {'X-HockeyAppToken': config.hockeyapp_token}
    r = requests.get(
        'https://rink.hockeyapp.net/api/2%s' % entrypoint,
        headers=headers, params=params)

    r.raise_for_status()
    return r

def hockeyapp_getall(entrypoint, config):
    pagination = {'per_page': 100} # to minimize number of requests
    r = hockeyapp_get(entrypoint, config, params=pagination).json()

    # determine the key attribute
    keys = set(r.keys())
    num_pages = r['total_pages'] if 'total_pages' in keys else 1
    candidate_keys = keys - set([
        'status', 'total_entries', 'total_pages', 'current_page', 'per_page'])
    assert len(candidate_keys) == 1, candidate_keys
    key_attr = candidate_keys.pop()

    entries = r[key_attr]
    if num_pages == 1:
        return entries

    num_entries = r['total_entries']
    for page in range(2, num_pages + 1):
        pagination['page'] = page
        r = hockeyapp_get(entrypoint, config, params=pagination).json()
        entries += r[key_attr]

        time.sleep(1.5) # throttling, 60 reqs/min

    assert len(entries) == num_entries, (entries, num_entries)
    return entries

def test_authentication(config):
    headers = {'X-HockeyAppToken': config.hockeyapp_token}
    r = requests.get('https://rink.hockeyapp.net/api/2/apps', headers=headers)
    assert r.status_code == 200

def test_error__non_200_status_code(config):
    with pytest.raises(requests.HTTPError):
        hockeyapp_get('/apps/INVALID_APP_ID/app_versions', config)

@pytest.mark.xfail
def test_rate_limit__http_xxx_error(config):
    with pytest.raises(requests.HTTPError) as excinfo:
        for attempts in range(100): # limit 60 requests/min, for each app ID
            logging.warn('Rate limiting: %s/100 ...', attempts + 1)
            hockeyapp_get('/apps/%s/crash_reasons' % config.hockeyapp_app_id, config)

    r = excinfo.value.response
    print(r.status_code)
    print(r.headers)
    print(r.text)
