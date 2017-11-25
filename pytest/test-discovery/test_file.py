import unittest

def test_method():
    assert True

def testmethod():
    assert False

class TestClass:

    def test_method(self):
        assert True

    def testmethod(self):
        assert False

class TestRun: # regular class

    @property
    def test_reports(self):
        assert False

class ClassTest:

    def test_method(self):
        assert False

    def testmethod(self):
        assert False

class MyTestSuite(unittest.TestCase):

    def test_method(self):
        assert True

    def testmethod(self):
        assert False

