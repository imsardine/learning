# -*- coding: utf-8 -*-
from flask import Flask, render_template_string
import jinja2

def test_undefined_variable__no_error():
    app = Flask(__name__)
    assert issubclass(app.jinja_env.undefined, jinja2.Undefined)

    @app.route('/')
    def endpoint():
        return render_template_string('foo = [{{bar}}]', foo='blabla')

    resp = app.test_client().get('/')

    # http://jinja.pocoo.org/docs/2.10/templates/#variables
    # If a variable or attribute does not exist, you will get back an undefined
    # value. What you can do with that kind of value depends on the application
    # configuration: the default behavior is to evaluate to an empty string if
    # printed or iterated over, and to fail for every other operation.
    assert resp.data == b'foo = []'

def test_undefined_variable__strict__raise_error(capsys, caplog, flask_ver):
    app = Flask(__name__)

    # http://jinja.pocoo.org/docs/2.10/api/#undefined-types
    # The closest to regular Python behavior is the StrictUndefined which
    # disallows all operations beside testing if it’s an undefined object.
    app.jinja_env.undefined = jinja2.StrictUndefined

    @app.route('/')
    def endpoint():
        return render_template_string('foo = [{{bar}}]', foo='blabla')

    resp = app.test_client().get('/')
    assert resp.status_code == 500

    out, err = capsys.readouterr()
    log = caplog.text
    dest = err if flask_ver[0] == 0 else log # Flask 1.x write errors as logs

    assert "UndefinedError: 'bar' is undefined" in dest, (out, err, log)

