from flask import Blueprint

blueprint= Blueprint('home', __name__)

@blueprint.route('/')
def welcome():
    return "Welcome!"

