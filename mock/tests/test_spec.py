import pytest
from mock import Mock, MagicMock, create_autospec

def test_spec__list_of_strings():
    mock = Mock(spec=['this', 'that'])

    assert 'this' in dir(mock) # created eagerly
    assert isinstance(mock.this, Mock)

    with pytest.raises(AttributeError):
        mock.other

def test_spec__class():
    mock = Mock(spec=Spec)
    attrs = dir(mock)

    assert 'class_attr' in attrs
    assert '_private_attr' not in attrs # constructor is not consulted

    assert 'method' in attrs
    mock.method('arg1', 'arg2') # signature is not respected

    assert 'prop_ro' in attrs
    mock.prop_ro = 'bla' # read-only is not respected

def test_spec__object():
    mock = Mock(spec=Spec())
    attrs = dir(mock)

    assert 'class_attr' in attrs
    assert '_private_attr' in attrs # constructor IS consulted

    assert 'method' in attrs
    mock.method('arg1', 'arg2') # signature is not respected

    assert 'prop_ro' in attrs
    mock.prop_ro = 'bla' # read-only is not respected

def test_autospec():
    mock = create_autospec(spec=Spec)
    attrs = dir(mock)

    assert 'class_attr' in attrs
    assert '_private_attr' not in attrs # constructor is not consulted

    assert 'method' in attrs
    with pytest.raises(TypeError):
        mock.method('arg1', 'arg2') # signature IS respected

    assert 'prop_ro' in attrs
    mock.prop_ro = 'bla' # read-only is NOT respected

class Spec:
    class_attr = 'class attribute'

    def __init__(self):
        self._private_attr = 'private attribute'

    def method(self, arg):
        return 'method'

    @property
    def prop_ro(self):
        return 'property'

