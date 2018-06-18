from flask import Flask

def test_teardown_appcontext():
    app = Flask(__name__)

    appcontext_called = []
    request_called = []

    @app.teardown_appcontext
    def on_appcontext_ends(exc):
        appcontext_called.append(True)

    @app.teardown_request
    def on_request_ends(exc):
        request_called.append(True)

    client = app.test_client()
    client.get('/')
    client.get('/')

    # Regardless of the naming, both teardown functions run at the end of
    # each request
    assert len(appcontext_called) == 2
    assert len(request_called) == 2