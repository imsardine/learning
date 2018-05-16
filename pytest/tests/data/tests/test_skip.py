import pytest

@pytest.mark.skip(reason='Reason for skipping')
def test_with_skip_mark__skipped():
    assert False

def test_without_skip_mark__not_skipped():
    pass
