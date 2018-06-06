from matchers import *

def test_version(cli):
    r = cli.run('make --version')
    assert r.out.splitlines()[0] == matches(r'GNU Make \d+\.\d+')

def test_default_make_file_and_target(cli):
    cli.src('Makefile', r"""
    hello:
    	@echo 'Hello, World!' # Inline comments passed to shell
    """)

    r1 = cli.run('make')
    r2 = cli.run('make hello')
    r3 = cli.run('make -f Makefile')
    r4 = cli.run('make -f Makefile hello')
    assert r1.out == r2.out == r3.out == r4.out == 'Hello, World!\n'

def test_variable_overriding(cli):
    cli.src('Makefile', r"""
    # Conditional assignment
    WHO ?= 'World'

    hello:
    	@echo Hello, $(WHO)'!' # Inline comments passed to shell
    """)

    assert cli.run('make').out == 'Hello, World!\n'
    assert cli.run('WHO=Make make').out == 'Hello, Make!\n'

