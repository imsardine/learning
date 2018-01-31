from flask import request
from flask import render_template, redirect, url_for
from flask import Blueprint
from wtforms import Form, StringField, validators

blueprint = Blueprint('hello', __name__, url_prefix='/hello', template_folder='templates')

@blueprint.route('/<somebody>')
def hello(somebody='World'):
    return 'Hello, %s!' % somebody

@blueprint.route('/', methods=['GET', 'POST'])
def hello_form():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        return redirect(url_for('hello.hello', somebody=form.name.data))

    return render_template('hello.html', form=form)

class HelloForm(Form):
    name = StringField('Name', [validators.DataRequired()])

