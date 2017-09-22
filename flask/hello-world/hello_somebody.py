from flask import Flask
app = Flask(__name__)

@app.route('/')
@app.route('/<somebody>')
def hello(somebody='World'):
    # Use two routes to implement optional URL parameters.
    return 'Hello, %s!' % somebody

