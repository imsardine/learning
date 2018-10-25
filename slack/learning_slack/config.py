import os

class Config():

    def __init__(self):
        self.slack_verification_token = os.environ['SLACK_VERIFICATION_TOKEN']
        self.slack_signing_secret = os.environ['SLACK_SIGNING_SECRET']
        self.slack_bot_token = os.environ['SLACK_BOT_TOKEN']