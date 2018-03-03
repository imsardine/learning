from mock import Mock
from mock import sentinel, call

def test_multiple_access__same_object():
    assert sentinel.this_object is sentinel.this_object
    assert sentinel.this_object is not sentinel.that_object

def test_argument_passing_and_return_value():
    def func(collaborator, arg):
        return collaborator.do_something(arg)

    collaborator = Mock()
    collaborator.do_something.return_value = sentinel.some_object

    result = func(collaborator, sentinel.func_arg)

    assert collaborator.mock_calls == [call.do_something(sentinel.func_arg)]
    assert result is sentinel.some_object

