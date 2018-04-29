def test_interval_comparison():
    num = 3 # between 2 and 4?

    assert num > 2 and num < 4
    assert 2 < num < 4 # interval comparison
