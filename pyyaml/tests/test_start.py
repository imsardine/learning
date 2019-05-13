from textwrap import dedent
import base64
import yaml
import pytest

def test_hello_world():
    content = dedent(r'''
    greeting: Hello
    to      : World
    ''')

    assert yaml.load(content) == {
        'greeting': 'Hello',
        'to': 'World',
    }

def test_null_literal():
    content = dedent(r'''
    null_value  : null
    null_string : 'null'
    ''')

    assert yaml.load(content) == {
        'null_value': None,
        'null_string': 'null',
    }

def test_boolean_literals():
    # https://yaml.org/type/bool.html
    content = dedent(r'''
    true_values : [y, Y, yes, Yes, YES, true, True, TRUE, on, On, ON]
    false_values: [n, N, no, No, NO, false, False, FALSE, off, Off, OFF]
    ''')

    # y|Y|n|N not Recognised as Booleans https://github.com/yaml/pyyaml/issues/247
    assert yaml.load(content) == {
        'true_values': ['y', 'Y'] + [True] * 9,
        'false_values': ['n', 'N'] + [False] * 9,
    }

def test_root_can_be_sequence():
    content = dedent(r'''
    - one
    - two
    ''')

    assert yaml.load(content) == ['one', 'two']

def test_root_can_be_scalar():
    assert yaml.load('null') == None
    assert yaml.load('true') == True
    assert yaml.load('false') == False

def test_multiline_base64():
    # cat hello.yml | base64 -w 10
    content = dedent(r'''
    hello_yaml: |
      Z3JlZXRpbm
      c6IEhlbGxv
      CnRvICAgIC
      AgOiBXb3Js
      ZA==
    ''')

    b64_chunks = yaml.load(content)['hello_yaml']
    content = base64.standard_b64decode(b64_chunks).decode('utf-8')

    assert content == dedent(r'''
    greeting: Hello
    to      : World
    ''').strip()

