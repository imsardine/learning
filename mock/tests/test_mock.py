import re
import pytest
from mock import Mock, MagicMock
from mock import call, DEFAULT

REPR_PATTERN = r'''<Mock(?: name='(?P<name>.+)')? id='\d+'>'''

def mock_name(mock):
    match = re.match(REPR_PATTERN, repr(mock))
    return match.group('name')

def test_mock_and_magicmock():
    assert issubclass(MagicMock, Mock)

def test_attr_access__mock__create_attr():
    mock = Mock()

    attr1 = mock.attr
    attr2 = mock.attr
    method = mock.method
    return_value1 = mock.method()
    return_value2 = mock.method()

    assert isinstance(attr1, Mock)
    assert isinstance(method, Mock)
    assert isinstance(return_value1, Mock)

    # return the same mock
    assert attr1 is attr2
    assert return_value1 is return_value2

def test_attr_access__magicmock__create_attr():
    mock = MagicMock()

    attr1 = mock.attr
    attr2 = mock.attr
    method = mock.method
    return_value1 = mock.method()
    return_value2 = mock.method()

    assert isinstance(attr1, MagicMock)
    assert isinstance(method, MagicMock)
    assert isinstance(return_value1, MagicMock)

    # return the same mock
    assert attr1 is attr2
    assert return_value1 is return_value2

def test_attr_access__magic_method__raise_error():
    mock = Mock()
    assert re.match(r"""<Mock id='\d+'>""", str(mock)) # __str__()

    with pytest.raises(AttributeError):
        mock.__len__() # len(mock)

def test_hasattr__create_attr_implicitly():
    mock = Mock()
    assert 'attr' not in dir(mock)

    assert hasattr(mock, 'attr')
    assert 'attr' in dir(mock)

def test_hasattr__delete_attr():
    mock = Mock()
    assert 'attr' not in dir(mock)

    del mock.attr # delete attr explicitly
    assert not hasattr(mock, 'attr')

    with pytest.raises(AttributeError):
        mock.attr

def test_return_value__fixed():
    mock = Mock()
    mock.method = Mock(return_value=3)

    assert mock.method() == 3
    assert mock.method('any', 'arguments') == 3

def test_return_value_and_side_effect():
    mock = Mock()
    mock.method = Mock(return_value=3)
    mock.method.side_effect= [4, 5, RuntimeError(), 6, DEFAULT]

    assert mock.method() == 4 # side_effect take precedence of return_value
    assert mock.method() == 5

    with pytest.raises(RuntimeError):
        mock.method()

    assert mock.method() == 6
    assert mock.method() == 3 # normal return value

    with pytest.raises(StopIteration): # return_value no more respected
        mock.method()

def test_mock_name__unnamed_and_named():
    unnamed = Mock()
    assert mock_name(unnamed) is None

    named = Mock(name='foo')
    assert mock_name(named) == 'foo'
    assert 'name' not in dir(named)

def test_mock_name__name_attr__not_respected():
    mock = Mock(name='foo')
    assert 'name' not in dir(mock)

    mock.configure_mock(name='bar')
    assert 'name' in dir(mock)
    assert mock.name == 'bar'
    assert mock_name(mock) == 'foo' # repr doesn't respect name attribute

def test_mock_name__attr_method_access():
    assert mock_name(Mock().attr) == 'mock.attr' # defaults to 'mock.'
    assert mock_name(Mock(name='foo').attr) == 'foo.attr' # propagated

    assert mock_name(Mock().method()) == 'mock.method()' # () indicates return value
    assert mock_name(Mock().method('args')) == 'mock.method()' # no args in the name
    assert mock_name(Mock().method('args').attr) == 'mock.method().attr'

def test_mock_and_method_calls():
    mock = MagicMock()

    mock()
    mock.attr()
    mock.attr.method()
    int(mock)
    int(mock.attr)

    assert mock.mock_calls == [
        call(),
        call.attr(),
        call.attr.method(),
        call.__int__(),
        call.attr.__int__()
    ]

    assert mock.method_calls == [
        # no calls to mock object itself, and to magic methods
        call.attr(),
        call.attr.method()
    ]

def test_attaching__unnamed_attr_assignment__propogated():
    parent = Mock()
    child = Mock() # unnamed
    assert mock_name(parent) is None

    assert mock_name(child) is None
    parent.child = child # attach
    assert mock_name(child) == 'mock.child' # renamed

    child.foo()
    assert parent.mock_calls == [call.child.foo()] # propogated

def test_attaching__named_attr_assignment__not_propogated():
    parent = Mock()
    child = Mock(name='named')
    assert mock_name(parent) is None

    assert mock_name(child) == 'named'
    parent.child = child # attach (assignment)
    assert mock_name(child) == 'named' # not renamed

    child.foo()
    assert parent.mock_calls == [] # NOT propogated

def test_attaching__attach_named__propogated():
    parent = Mock()
    child = Mock(name='named')
    assert mock_name(parent) is None

    assert mock_name(child) == 'named'
    parent.attach_mock(child, 'child') # attach (API)
    assert mock_name(child) == 'mock.child' # renamed

    child.foo()
    assert parent.mock_calls == [call.child.foo()] # propogated

def test_attaching__attr_method_access_and_return_value():
    mock = Mock()

    # both attribute and return value get attached automatically
    rvalue1 = mock.foo.bar()
    rvalue2 = mock.foo().bar()

    assert mock_name(rvalue1) == 'mock.foo.bar()'
    assert mock_name(rvalue2) == 'mock.foo().bar()'
    assert mock.mock_calls == [
        call.foo.bar(),
        call.foo(),
        call.foo().bar()
    ]

