import types

def test_none_singleton():
    assert isinstance(None, types.NoneType)

class Negator(object):

    def __eq__(self, other):
        return not other # doesn't make sense

def test_none_identity():
    none = None
    thing = Negator()

    assert none is None # singleton
    assert thing is not None

def test_none_equality():
    none = None
    thing = Negator()

    assert none == None
    assert not (none != None)

    assert thing == None # dependes on __eq__
    assert thing != None

