# -*- coding: utf-8 -*-
import os
from flask import Flask, request, abort, jsonify
import requests

SEND_API = 'https://graph.facebook.com/v2.6/me/messages'
WEBHOOK_VERIFY_TOKEN = os.environ['WEBHOOK_VERIFY_TOKEN']
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
APP_SECRET = os.environ['APP_SECRET']

app = Flask(__name__)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET': # GET for webhook verification
        return verify_webhook()

    # POST for message events
    assert request.is_json
    data = request.get_json()

    if data['object'] == 'page':
        for entry in data['entry']:
            for event in entry['messaging']:
                if 'message' not in event:
                    abort(400) # Unknown event
                on_message_event(event)
    else:
        abort(400) # Bad Request

    return ''

def verify_webhook(mode, verify_token):
    query_params = request.args
    hub_mode = query_params.get('hub.mode')
    hub_verify_token = query_params.get('hub.verify_token')

    if hub_verify_token != WEBHOOK_VERIFY_TOKEN:
        abort(403) # Forbidden
    elif hub_mode == 'subscribe':
        return query_params['hub.challenge']

def on_message_event(event):
    app.logger.info('Message data: %s', event)

    timestamp = event['timestamp']
    sender_id = event['sender']['id']
    recipient_id = event['recipient']['id']
    message = event['message']

    if 'text' in message:
        handle_text_message(sender_id, message['text'])
    elif 'attachments' in message:
        pass
    else:
        abort(400)

def handle_text_message(sender_id, message):
    params = {'access_token': PAGE_ACCESS_TOKEN}

    data = {
        'recipient': {
            'id': sender_id
        },
        'message': {
            'text': message
        }
    }

    resp = requests.post(SEND_API, params=params, json=data)
    app.logger.info('Message posted: message = %s, response = %s', data, resp.json())

if __name__ == '__main__':
    app.run()

