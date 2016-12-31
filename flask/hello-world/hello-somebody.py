from flask import Flask
app2 = Flask(__name__)

@app2.route('/')
@app2.route('/<somebody>')
def hello(somebody='World'):
    # Use two routes to implement optional URL parameters.
    return 'Hello, %s!' % somebody

# As of Flask 0.11, use flask command to launch your app. For example:
#
# $ export FLASK_DEBUG=1 # enable debug mode
# $ export FLASK_APP=hello.py
# $ flask run
#  * Running on http://127.0.0.1:5000/
#
# if __name__ == '__main__':
#    app.run()
#
