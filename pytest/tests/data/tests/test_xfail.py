import pytest

def test_without_xfail_mark__passed():
    pass

@pytest.mark.xfail
def test_expected_to_fail__failed__xfailed():
    assert False

@pytest.mark.xfail
def test_expected_to_fail__passed__xpassed():
    pass
