import re

def test_named_group():
    pattern = r'(?P<number>\d+(?:.\d+)?)(?P<unit>K)? Ratings'
    match = re.search(pattern, '8723 Ratings')
    assert match.group('number') == '8723'
    assert match.group('unit') is None

    match = re.search(pattern, '8.7K Ratings')
    assert match.group('number') == '8.7'
    assert match.group('unit') == 'K'

