import os
from flask import Flask
app = Flask(__name__)

if os.getenv('UWSGI_DEBUG'):
    app.debug = True
    from werkzeug.debug import DebuggedApplication
    app.wsgi_app = DebuggedApplication(app.wsgi_app, evalex=True, pin_security=False)

@app.route('/')
@app.route('/<somebody>')
def hello(somebody='World'):
    # Use two routes to implement optional URL parameters.
    assert False, "Runtime Error!"
    return 'Hello, %s!' % somebody

