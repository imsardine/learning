from matchers import *

def test_version(cli):
    r = cli.run('make --version')
    assert r.out.splitlines()[0] == matches(r'GNU Make \d+\.\d+')

def test_default_make_file_and_target(cli):
    r1 = cli.run('make', cwd='hello-world')
    r2 = cli.run('make hello', cwd='hello-world')
    r3 = cli.run('make -f hello-world/Makefile')
    assert r1.out == r2.out == r3.out == 'Hello, World!\n'

def test_hello_world(cli):
    r = cli.run('make -f hello-world/Makefile hello')
    assert r.out == 'Hello, World!\n'

def test_hello_world_customization(cli):
    r = cli.run('WHO=Make make -f hello-world/Makefile hello')
    assert r.out == 'Hello, Make!\n'

