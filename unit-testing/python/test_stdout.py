from StringIO import StringIO
import unittest2 as unittest
from mock import patch

def say_hello(who=None):
    who = who or 'World'
    print 'Hello, %s!' % who

class StandardOutputTest(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_hello_default(self, mock_stdout):
        say_hello()
        self.assertEqual(mock_stdout.getvalue(), 'Hello, World!\n')

    @patch('sys.stdout', new_callable=StringIO)
    def test_hello_someone(self, mock_stdout):
        say_hello('Success')
        self.assertEqual(mock_stdout.getvalue(), 'Hello, Success!\n')

