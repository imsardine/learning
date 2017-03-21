import unittest
import tempfile
import uuid
import os
import json
import argparse

# An OAuth 2.0 client.
# https://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html
from oauth2client import client

# Command-line tools for authenticating via OAuth 2.0
# https://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html
from oauth2client import tools  

# Store and retrieve a single credential to and from a file.
# https://oauth2client.readthedocs.io/en/latest/source/oauth2client.file.html#oauth2client.file.Storage
from oauth2client.file import Storage

# https://developers.google.com/sheets/api/guides/authorizing#OAuth2Scope
SCOPE = 'https://www.googleapis.com/auth/spreadsheets.readonly'

CLIENT_SECRET_FILE = 'client_secret.json'

class OAuth2Test(unittest.TestCase):

    def test_auth(self):
        with open(CLIENT_SECRET_FILE, 'rb') as f:
            client_secret = json.load(f)['installed']['client_secret']
        credential_filename = self._get_tempfile_name()

        storage = Storage(credential_filename)
        self.assertIsNone(storage.get())

        # Create a Flow from a clientsecrets file.
        # https://oauth2client.readthedocs.io/en/latest/source/oauth2client.client.html#oauth2client.client.flow_from_clientsecrets
        flow = client.flow_from_clientsecrets(filename=CLIENT_SECRET_FILE, scope=SCOPE)

        # Core code for a command-line application.
        # https://oauth2client.readthedocs.io/en/latest/source/oauth2client.tools.html#oauth2client.tools.run_flow
        tools.run_flow(flow, storage) 
        with open(credential_filename, 'rb') as f:
            self.assertEqual(json.load(f)['client_secret'], client_secret)

    def test_auth_noauth_local_webserver(self):
        with open(CLIENT_SECRET_FILE, 'rb') as f:
            client_secret = json.load(f)['installed']['client_secret']
        credential_filename = self._get_tempfile_name()

        storage = Storage(credential_filename)
        self.assertIsNone(storage.get())

        flow = client.flow_from_clientsecrets(filename=CLIENT_SECRET_FILE, scope=SCOPE)
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args(['--noauth_local_webserver'])
        tools.run_flow(flow, storage, flags) 

        with open(credential_filename, 'rb') as f:
            self.assertEqual(json.load(f)['client_secret'], client_secret)

    def _get_tempfile_name(self):   
        return os.path.join(tempfile.gettempdir(), uuid.uuid4().hex)

if __name__ == '__main__':
    unittest.main()

