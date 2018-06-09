import re
from textwrap import dedent

__all__ = ['matches', 'like', 'contains']

class _RegexMatcher():

    def __init__(self, pattern):
        self._pattern = pattern

    def __eq__(self, other):
        return re.match(self._pattern, other, re.DOTALL)

def matches(pattern):
    return _RegexMatcher(pattern)

class _ContainsMatcher():

    def __init__(self, substr):
        self._substr = substr

    def __eq__(self, other):
        return self._substr in other

def contains(substr):
    return _ContainsMatcher(substr)

ELLIPSIS = re.escape('...')
INDENTED_LITERAL = re.compile(r'^\n?(?P<content>.*)\n?\s*$', re.DOTALL)

def like(template):
    match = INDENTED_LITERAL.match(template)
    assert match, template

    content = dedent(match.group('content'))
    pattern = re.escape(content).replace(ELLIPSIS, '.+')

    return _RegexMatcher(pattern)

