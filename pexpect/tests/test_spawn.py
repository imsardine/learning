import pexpect
import pytest

def test_command_not_shell(cli):
    # https://pexpect.readthedocs.io/en/stable/FAQ.html
    # Why don't shell pipe and redirect (| and >) work when I spawn a command?
    cli.src('hello.py', '''
        from __future__ import print_function
        import os

        who = os.getenv('WHO', 'World')
        print('Hello, %s!' % who)
    ''')

    cmdline = 'WHO=Pexpect python hello.py'

    with pytest.raises(Exception) as exec_info:
        pexpect.spawn('WHO=Pexpect python hello.py', encoding='utf-8')
    assert str(exec_info.value) == 'The command was not found or was not executable: WHO=Pexpect.'

    child = pexpect.spawn('bash', ['-c', cmdline], encoding='utf-8')
    child.expect(pexpect.EOF)

    assert child.before == 'Hello, Pexpect!\r\n'

def test_stderr_in_output(cli):
    cli.src('hello.py', """
        from __future__ import print_function
        import os, sys

        who = os.getenv('WHO')
        if who is None:
            print("WHO defaults to 'World'.", file=sys.stderr)
            who = 'World'

        print('Hello, %s!' % who)
    """)

    child = pexpect.spawn('python hello.py', encoding='utf-8')
    child.expect(u'Hello, World!')

    assert child.before == "WHO defaults to 'World'.\r\n"
