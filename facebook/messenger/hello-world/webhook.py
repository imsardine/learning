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
                timestamp = event['timestamp']
                sender_id = event['sender']['id']
                recipient_id = event['recipient']['id']

                if 'message' in event:
                    on_message_event(timestamp, sender_id, event['message'])
                elif 'postback' in event:
                    on_postback_event(timestamp, sender_id, event['postback'])
                else:
                    abort(400) # Unknown event
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

def on_message_event(timestamp, sender_id, message):
    if 'text' in message:
        handle_text_message(sender_id, message['text'])
    elif 'attachments' in message:
        pass
    else:
        abort(400)

def on_postback_event(timestamp, sender_id, postback):
    payload = postback['payload']
    send_text(sender_id, 'Thanks for selecting %s' % payload)

def send_text(recipient_id, text):
    send_message(recipient_id, {'text': text})

def send_message(recipient_id, message):
    params = {'access_token': PAGE_ACCESS_TOKEN}
    data = {
        'recipient': {
            'id': recipient_id
        },
        'message': message,
    }

    resp = requests.post(SEND_API, params=params, json=data)
    app.logger.info('Message posted: message = %s, response = %s', data, resp.json())

def handle_text_message(sender_id, text):
    if u'吃什麼' in text:
        send_text(sender_id, u'Judy 爸爸說：不知道')
    elif text == 'generic':
        send_message(sender_id, demo_generic_template(sender_id, text))
    else:
        send_text(sender_id, text)

def demo_generic_template(sender_id, message):
    return {
        'attachment': {
            'type': 'template', # structured message
            'payload': {
                'template_type': 'generic',
                'elements': [
                    {
                        'title': 'rift',
                        'subtitle': 'Next-generation virtual reality',
                        'item_url': 'https://www.oculus.com/en-us/rift/',
                        'image_url': 'http://messengerdemo.parseapp.com/img/rift.png',
                        'buttons': [
                            {
                                'type': 'web_url',
                                'url': 'https://www.oculus.com/en-us/rift/',
                                'title': 'Open Web URL',
                            },
                            {
                                'type': 'postback',
                                'title': 'Call Postback',
                                'payload': 'Payload for first bubble'
                            }
                        ],
                    },
                    {
                        'title': 'touch',
                        'subtitle': 'Your Hands, Now in VR',
                        'item_url': 'https://www.oculus.com/en-us/touch/',
                        'image_url': 'http://messengerdemo.parseapp.com/img/touch.png',
                        'buttons': [
                            {
                                'type': 'web_url',
                                'url': 'https://www.oculus.com/en-us/touch/',
                                'title': 'Open Web URL',
                            },
                            {
                                'type': 'postback',
                                'title': 'Call Postback',
                                'payload': 'Payload for second bubble'
                            }
                        ],
                    },
                ],
            }
        }
    }

if __name__ == '__main__':
    app.run()

