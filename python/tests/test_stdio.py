from . import *
import os, sys
import pexpect
import pytest

@py2_only
def test_keyboard_input_py2(workspace):
    # https://docs.python.org/2/library/functions.html#raw_input
    workspace.src('keyboard_input.py', """
        input = raw_input('Type something: ')
        print 'You just typed: [%s]' % input
    """)

    os.chdir(workspace.workdir) # workaround
    child = pexpect.spawn('python keyboard_input.py')
    child.expect('Type something: ')
    child.sendline('blah blah blah')

    child.expect('You just typed: \[(?P<input>.+?)\]')
    assert child.match.group('input') == 'blah blah blah'

@py3_later
def test_keyboard_input_py3(workspace):
    # https://docs.python.org/3/library/functions.html#input
    # https://docs.python.org/3/whatsnew/3.0.html#index-32
    workspace.src('keyboard_input.py', """
        input = input('Type something: ')
        print('You just typed: [%s]' % input)
    """)

    os.chdir(workspace.workdir) # workaround
    child = pexpect.spawn('python keyboard_input.py', encoding='utf-8')
    child.expect('Type something: ')
    child.sendline('blah blah blah')

    child.expect('You just typed: \[(?P<input>.+?)\]')
    print(type(child.match.group('input')))
    assert child.match.group('input') == 'blah blah blah'
