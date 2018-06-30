import pytest

def test_hello_world(shell):
    shell.src('hello.c', r"""
    #include <stdio.h>

    int main() {
        printf("Hello, World!\n");
        return 0;
    }
    """)

    shell.run('make hello')
    r = shell.run('./hello')

    assert r.out == 'Hello, World!\n'

def test_printf__leading_zeros(cprog):
    out = cprog.run(r"""
    int num = 8;
    printf("The next one is #%03d", num);
    """)

    assert out == 'The next one is #008'

@pytest.fixture
def cprog(shell):
    return _CProgram(shell)

class _CProgram():

    def __init__(self, shell):
        self._shell = shell

    def run(self, main_body):
        self._shell.src('main.c', """
        #include <stdio.h>

        int main() {
            %s
        }""" % main_body)

        self._shell.run('make main')
        r = self._shell.run('./main')

        return r.out

