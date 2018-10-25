import logging
import json
from flask import Flask, request, abort, jsonify
from .config import Config

logging.basicConfig(level=logging.DEBUG)

logger = logging.getLogger(__name__)
config = Config()
app = Flask(__name__)

@app.route('/slack/slashcmd', methods=['GET', 'POST'])
def slash_command_handler():
    # Slack may occasionally send a simple GET request to verify the URL and certificate.
    if request.method == 'GET' and request.args.get('ssl_check', None):
        return

    if request.form['token'] != config.slack_verification_token:
        abort(401) # Unauthorized

    user = request.form['user_name']
    cmd = request.form['command']
    args = request.form['text']

    text = 'Hello, %s! Hello, World!' % user
    attached = {
        'callback_id': 'voila',
        'text': 'And here is the original command:\n%s %s' % (cmd, args),
        'actions': [
            {
                'name': 'type',
                'text': 'What kind of question?',
                'type': 'select',
                'options': [
                    {'text': 'Type 1', 'value': '1' + args },
                    {'text': 'Type 2', 'value': '2' + args },
                ],
            },
        ]
    }

    # ephemeral, therefore no original_message in subsequent action payload
    return jsonify({'text': text, 'attachments': [attached]})

@app.route('/slack/action', methods=['POST'])
def action_handler():
    payload = json.loads(request.form['payload'])
    user = payload['user']['name']
    value = payload['actions'][0]['selected_options'][0]['value']
    decision, question = value[0], value[1:]
    logger.error('DECISION: %s' % decision)

    channel = 'private-channel-%s' % decision

    from slackclient import SlackClient
    slack = SlackClient(config.slack_bot_token)
    message = "<@%s> has a question, let's give him/her a favor ~\n\n%s" % (user, question)
    slack.api_call('chat.postMessage', channel=channel, text=message)

    return jsonify({'text': "The question has been redirected to support teams."})

