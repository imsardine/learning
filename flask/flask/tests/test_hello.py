def test_hello__none__hello_world(client):
    resp = client.get('/hello/')
    assert resp.data == 'Hello, World!'

def test_hello__somebody__hello_somebody(client):
    resp = client.get('/hello/Flask')
    assert resp.data == 'Hello, Flask!'
