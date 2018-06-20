from matchers import *

def test_version(shell):
    r = shell.run('make --version')
    assert r.out.splitlines()[0] == matches(r'GNU Make \d+\.\d+')

def test_default_make_file_and_target(shell):
    shell.src('Makefile', r"""
    hello:
    	@echo 'Hello, World!' # Inline comments passed to shell
    """)

    r1 = shell.run('make')
    r2 = shell.run('make hello')
    r3 = shell.run('make -f Makefile')
    r4 = shell.run('make -f Makefile hello')
    assert r1.out == r2.out == r3.out == r4.out == 'Hello, World!\n'

def test_variable_overriding(shell):
    shell.src('Makefile', r"""
    # Conditional assignment
    WHO ?= 'World'

    hello:
    	@echo Hello, $(WHO)'!' # Inline comments passed to shell
    """)

    assert shell.run('make').out == 'Hello, World!\n'
    assert shell.run('WHO=Make make').out == 'Hello, Make!\n'

