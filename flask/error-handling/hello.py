from flask import Flask
from flask import render_template
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

class PermissionDeniedError(Exception):

    def __init__(self, resource, permission):
        self.resource = resource
        self.permission = permission

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/secret/<resource>')
def hello(resource):
    # trigger permission_denied(error)
    raise PermissionDeniedError(resource, 'VIEW')

@app.route('/error')
def error():
    # trigger uncaught_exception(error)
    raise RuntimeError('Something wrong!!')

@app.errorhandler(404)
def not_found(error):
    assert isinstance(error, HTTPException)
    return render_template('404.html'), 404

@app.errorhandler(PermissionDeniedError)
def permission_denied(error):
    rollback_db_transaction()
    return render_template('permission-denied.html', error=error), 503

@app.errorhandler(Exception)
def uncaught_exception(error):
    rollback_db_transaction()
    return 'Uncaught Exception: %s' % error, 500

def rollback_db_transaction():
    pass # db.session.rollback()

