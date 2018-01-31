def test_hello__somebody__hello_somebody(client):
    resp = client.get('/hello/Flask')
    assert resp.data == 'Hello, Flask!'

def test_hello_form_view(client):
    resp = client.get('/hello/')

    assert resp.status_code == 200
    assert 'Say hello to' in resp.data

def test_hello_form_submission__empty__rerender(client):
    resp = client.post('/hello/', data=dict(name=''))

    assert resp.status_code == 200
    assert 'Say hello to' in resp.data

def test_hello_form_submission__not_empty__say_hello(client):
    resp = client.post('/hello/', data=dict(name='Flask'))

    assert resp.status_code == 302
    assert resp.headers.get('Location') == 'http://localhost/hello/Flask'
