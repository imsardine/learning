from flask import Flask, request, abort, jsonify
app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # Slack may occasionally send a simple GET request to verify the URL and certificate.
    if request.method == 'GET' and request.args.get('ssl_check', None):
        return

    if request.form['token'] != '...':
        abort(401) # Unauthorized

    user = request.form['user_name']
    cmd = request.form['command']
    args = request.form['text']

    text = 'Hello, %s! Hello, World!' % user
    attached = { 'text': 'And here is the original command:\n%s %s' % (cmd, args) }

    return jsonify({ 'text': text, 'attachments': [attached]})

