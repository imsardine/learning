import re

__all__ = ['regex', 'contains']

class _RegexMatcher():

    def __init__(self, pattern):
        self._pattern = pattern

    def __eq__(self, other):
        return re.match(pattern, other)

def matches(pattern):
    return _RegexMatcher(pattern)

class _ContainsMatcher():

    def __init__(self, substr):
        self._substr = substr

    def __eq__(self, other):
        return self._substr in other

def contains(substr):
    return _ContainsMatcher(substr)
