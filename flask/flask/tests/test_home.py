def test_get(client):
    resp = client.get('/')

    assert resp.status == '200 OK'
    assert resp.data == 'Welcome!'

