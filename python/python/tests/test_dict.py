def test_empty_dict():
    assert dict() == {}

def test_construction():
    d1 = {'one': 1, 'two': 2, 'three': 3}
    d2 = dict({'one': 1}, two=2, three=3)
    d3 = dict([('one', 1)], two=2, three=3)

    assert d1 == d2 == d3

