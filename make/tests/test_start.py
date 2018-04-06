def test_version(cli):
    out, _, _ = cli.run('make --version')
    assert out.splitlines()[0] == matches(r'GNU Make \d+\.\d+')

def test_hello_world(cli):
    out, _, _ = cli.run('make', cwd='hello-world')
    assert out == 'Hello, World!\n'

def test_hello_world_customization(cli):
    out, _, _ = cli.run('WHO=Make make', cwd='hello-world')
    assert out == 'Hello, Make!\n'

import re

class _RegexMatcher():

    def __init__(self, regex):
        self._regex = regex

    def __eq__(self, other):
        return re.match(self._regex, other)

def matches(regex):
    return _RegexMatcher(regex)

class _ContainsMatcher():

    def __init__(self, substr):
        self._substr = substr

    def __eq__(self, other):
        return self._substr in other

def contains(substr):
    return _ContainsMatcher(substr)
