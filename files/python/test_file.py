import unittest2 as unittest
from os import path

class FileTest(unittest.TestCase):

    def setUp(self):
        self._input_file = path.join(path.dirname(__file__), 'input.txt')

    def test_read_chunks(self):
        with open(self._input_file, 'rb') as f:
            size = 7 # chunkN + newline
            self.assertEqual(f.read(size), 'chunk1\n')
            self.assertEqual(f.read(size), 'chunk2\n')
            self.assertEqual(f.read(size), '\n')
            self.assertEqual(f.read(size), '') # EOF reached

        with open(self._input_file, 'rb') as f:
            size = 7 + 2
            self.assertEqual(f.read(size), 'chunk1\nch')
            self.assertEqual(f.read(size), 'unk2\n\n') # less than chunk size
            self.assertEqual(f.read(size), '') # EOF reached

    def test_read_lines(self):
        with open(self._input_file, 'rb') as f:
            self.assertEqual(f.readline(), 'chunk1\n')
            self.assertEqual(f.readline(), 'chunk2\n')
            self.assertEqual(f.readline(), '\n')
            self.assertEqual(f.readline(), '')

        with open(self._input_file, 'rb') as f:
            self.assertEqual(f.readlines(), ['chunk1\n', 'chunk2\n', '\n'])

