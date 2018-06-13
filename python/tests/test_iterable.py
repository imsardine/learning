def test_enumerate__return_iterator():
    try:
        next(enumerate([1, 2, 3])) # __next__()
        assert True
    except:
        assert False

def test_enumerate__list():
    items = []
    for item in enumerate(['a', 'b', 'c']):
        items.append(item)

    # iterator of 2-tuple (index, value)
    assert items == [(0, 'a'), (1, 'b'), (2, 'c')]

