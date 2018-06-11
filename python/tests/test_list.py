def test_sorting__sorted():
    versions = ['10.0.01', '11.3.00', '9.8.12', '9.8.00']
    assert sorted(versions, key=lambda v: map(int, v.split('.'))) == \
        ['9.8.00', '9.8.12', '10.0.01', '11.3.00']

def test_sorting__sort_in_place():
    versions = ['10.0.01', '11.3.00', '9.8.12', '9.8.00']
    versions.sort(key=lambda v: map(int, v.split('.')))

    assert versions == ['9.8.00', '9.8.12', '10.0.01', '11.3.00']

