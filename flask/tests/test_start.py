import requests
import pytest

def test_hello_world(shell, flask_ver):
    shell.src('hello.py', """
    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'
    """)

    import flask
    if flask_ver[0] == 0: # 0.x
        message = """
        | * Serving Flask app "hello"
        | * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
        """
    else: # 1.x
        message = """
        | * Serving Flask app "hello.py"
        | * Environment: production
        |\x1b[31m   WARNING: Do not use the development server in a production environment.\x1b[0m
        |\x1b[2m   Use a production WSGI server instead.\x1b[0m
        | * Debug mode: off
        | * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
        """

    with shell.spawn('FLASK_APP=hello.py flask run') as p:
        p.expect_exact(message)

        resp = requests.get('http://localhost:5000')
        assert resp.text == 'Hello, World!'

def test_hello__somebody__hello_somebody(client):
    resp = client.get('/hello/Flask')
    assert resp.data == b'Hello, Flask!'

def test_hello_form_view(client):
    resp = client.get('/hello/')

    assert resp.status_code == 200
    assert b'Say hello to' in resp.data

def test_hello_form_submission__empty__rerender(client):
    resp = client.post('/hello/', data=dict(name=''))

    assert resp.status_code == 200
    assert b'Say hello to' in resp.data

def test_hello_form_submission__not_empty__say_hello(client):
    resp = client.post('/hello/', data=dict(name='Flask'))

    assert resp.status_code == 302
    assert resp.headers.get('Location') == 'http://localhost/hello/Flask'
