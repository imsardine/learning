import re

def test_named_group():
    pattern = r'(?P<number>\d+(?:.\d+)?)(?P<unit>K)? Ratings'
    match = re.search(pattern, '8723 Ratings')
    assert match.group('number') == '8723'
    assert match.group('unit') is None

    match = re.search(pattern, '8.7K Ratings')
    assert match.group('number') == '8.7'
    assert match.group('unit') == 'K'

def test_substitution__look_ahead_behind():
    origin = 'Hello, World! Have a nice day.'
    #           ^-- replace it

    # re.sub(pattern, repl, string), replace match.group(0)
    replaced = re.sub(r'(?<=Hello, )\w+(?=\! .+)', 'Regex', origin)
    assert replaced == 'Hello, Regex! Have a nice day.'

