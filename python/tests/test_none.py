import types

def test_singleton(py2):
    if py2:
        assert isinstance(None, types.NoneType)
    else:
        # https://stackoverflow.com/questions/21706609
        assert type(None)() is None

class Negator(object):

    def __eq__(self, other):
        return not other # doesn't make sense

    def __ne__(self, other): # requried for py2
        return not self.__eq__(other)

def test_comparison__use_identity():
    none = None
    thing = Negator()

    assert none is None # singleton
    assert thing is not None

def test_comparison__donot_use_equality():
    none = None
    thing = Negator()

    assert none == None
    assert not (none != None)

    # weird? the result dependes on thing.__eq__()
    assert thing == None
    assert not (thing != None)
