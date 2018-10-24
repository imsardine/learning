import os

class Config():

    def __init__(self):
        self.verification_token = os.environ['VERIFICATION_TOKEN']