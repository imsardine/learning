from flask import Blueprint

blueprint = Blueprint('hello', __name__, url_prefix='/hello')

@blueprint.route('/')
@blueprint.route('/<somebody>')
def hello(somebody='World'):
    return 'Hello, %s!' % somebody

