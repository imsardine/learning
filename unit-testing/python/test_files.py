import unittest2 as unittest
from mock import MagicMock, patch, mock_open, call
import files

class Test(unittest.TestCase):

    @patch('files.open', mock_open(read_data='content'), create=True)
    def test_read(self):
        f = files.open.return_value
        self.assertEqual(f.read.return_value, 'content') # read() always returns 'content'

        self.assertEqual(files.read('pathname'), 'content')
        files.open.assert_called_once_with('pathname', 'rb')

    @patch('files.open', mock_open(), create=True)
    def test_read_chunks(self):
        f = files.open.return_value
        f.read.side_effect = ['chunk1\n', 'chunk2\n', '\n', ''] # for each read(size)

        self.assertEqual(files.read_chunks('pathname', 7), ['chunk1\n', 'chunk2\n', '\n'])
        files.open.assert_called_once_with('pathname', 'rb')
        self.assertEqual(f.read.mock_calls, [call(7)] * 4)

    @patch('files.open', mock_open(), create=True)
    def test_readlines(self):
        f = files.open.return_value
        self.assertIsInstance(f.readline.return_value, MagicMock) # not configured
        self.assertIsNone(f.readline.side_effect)
        f.readlines.return_value = ['chunk1\n', 'chunk2\n', '\n'] # mock out readlines()

        self.assertEqual(files.readlines('pathname'), ['chunk1\n', 'chunk2\n', '\n'])
        files.open.assert_called_once_with('pathname', 'rb')
        f.readlines.assert_called_once_with()

    @patch('files.open', mock_open(), create=True)
    def test_readlines_accumulated(self):
        f = files.open.return_value
        f.readline.side_effect = ['chunk1\n', 'chunk2\n', '\n', ''] # mock out readline()

        self.assertEqual(files.readlines_accumulated('pathname'), ['chunk1\n', 'chunk2\n', '\n'])
        files.open.assert_called_once_with('pathname', 'rb')
        self.assertEqual(f.readline.mock_calls, [call()] * 4)

