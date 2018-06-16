import sys
import pexpect
import pytest

py2_only = pytest.mark.skipif(sys.version_info[0] >= 3, reason='Python 2')
py3_later = pytest.mark.skipif(sys.version_info[0] <= 2, reason='Python 3+')

HELLO_PY = """\
    from __future__ import print_function
    import sys

    input_func = input if sys.version_info[0] >= 3 else raw_input
    name = input_func("What's your name: ")

    print("Hello, %s!" % name)
    print('Have a nice day!')
"""

@py2_only
def test_hello_world_py2(cli):
    cli.src('hello.py', HELLO_PY)

    child = pexpect.spawn('python hello.py')
    child.expect("What's your name: ")

    child.sendline('Pexpect') # user input
    child.expect('Hello, (?P<who>.+?)!')

    # `after` and `match` for verification
    assert child.after == 'Hello, Pexpect!'
    assert child.match.group('who') == 'Pexpect'

    # remaining output, including linefeed (\r\n)
    child.expect(pexpect.EOF)
    assert child.before == '\r\nHave a nice day!\r\n'

@py3_later
def test_hello_world_py3__bytes_mode(cli):
    cli.src('hello.py', HELLO_PY)

    # defaults to bytes mode (no encoding arg)
    child = pexpect.spawn('python hello.py')
    child.expect("What's your name: ")

    child.sendline('Pexpect') # user input
    child.expect('Hello, (?P<who>.+?)!')

    # `after` and `match` for verification
    assert child.after == b'Hello, Pexpect!' # 'b' prefix is required
    assert child.match.group('who') == b'Pexpect'

    # remaining output, including linefeed (\r\n)
    child.expect(pexpect.EOF)
    assert child.before == b'\r\nHave a nice day!\r\n'

@py3_later
def test_hello_world_py3__unicode_mode(cli):
    cli.src('hello.py', HELLO_PY)

    # unicode mode
    child = pexpect.spawn('python hello.py', encoding='utf-8')
    child.expect("What's your name: ")

    child.sendline('Pexpect') # user input
    child.expect('Hello, (?P<who>.+?)!')

    # `after` and `match` for verification
    assert child.after == 'Hello, Pexpect!'
    assert child.match.group('who') == 'Pexpect'

    # remaining output, including linefeed (\r\n)
    child.expect(pexpect.EOF)
    assert child.before == '\r\nHave a nice day!\r\n'
