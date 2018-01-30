from flask import Flask

def create_app():
    app = Flask(__name__)

    from myapp.home import blueprint as home
    from myapp.hello import blueprint as hello
    app.register_blueprint(home)
    app.register_blueprint(hello)

    return app
