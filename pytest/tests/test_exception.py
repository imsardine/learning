import sys, re
import pytest

def test_assert_exception__verify_type_only():
    with pytest.raises(ZeroDivisionError):
        1 / 0

def test_assert_exception__verify_details_as_well():
    with pytest.raises(IndexError) as excinfo:
        ()[0]

    assert excinfo.type == IndexError
    assert isinstance(excinfo.value, excinfo.type)
    assert str(excinfo.value) == 'tuple index out of range'

@pytest.mark.skipif(sys.version_info[0] >=3, reason='py3-')
def test_assert_exception__py2_message_attr():
    with pytest.raises(IndexError) as excinfo:
        ()[0]
    assert excinfo.value.message == 'tuple index out of range'

@pytest.mark.skipif(sys.version_info[0] <= 2, reason='py3+')
def test_assert_exception__py3_message_attr__no_attr_error():
    with pytest.raises(IndexError) as excinfo:
        ()[0]

    with pytest.raises(AttributeError) as excinfo2:
        assert excinfo.value.message == '...'

    # use str() to get string representation
    assert str(excinfo2.value) == "'IndexError' object has no attribute 'message'"

def test_assert_exception__match_string_representation():
    # match kwarg uses re.search() internally
    with pytest.raises(IndexError, match=r'index out of range'):
        ()[0]

    # exactly match isn't handy
    match = '^%s$' % re.escape('tuple index out of range')
    with pytest.raises(IndexError, match=match):
        ()[0]