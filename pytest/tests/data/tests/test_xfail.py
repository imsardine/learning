import pytest

def test_without_xfail_mark__passed():
    pass

@pytest.mark.xfail(reason='Reason for expecting to fail (xfailed)')
def test_expected_to_fail__failed__xfailed():
    assert False

@pytest.mark.xfail(reason='Reason for expecting to fail (xpassed)')
def test_expected_to_fail__passed__xpassed():
    pass
