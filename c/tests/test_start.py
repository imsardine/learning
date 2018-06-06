import pytest

def test_hello_world(cli):
    cli.src('hello.c', r"""
        #include <stdio.h>

        int main() {
            printf("Hello, World!\n");
            return 0;
        }
    """)

    cli.run('make hello')
    r = cli.run('./hello')

    assert r.out == 'Hello, World!\n'

def test_printf__leading_zeros(cprog):
    out = cprog.run(r"""
        int num = 8;
        printf("The next one is #%03d", num);
    """)

    assert out == 'The next one is #008'

@pytest.fixture
def cprog(cli):
    return _CProgram(cli)

class _CProgram():

    def __init__(self, cli):
        self._cli = cli

    def run(self, main_body):
        self._cli.src('main.c', """\
            #include <stdio.h>

            int main() {
                %s
            }""" % main_body)

        self._cli.run('make main')
        r = self._cli.run('./main')

        return r.out

