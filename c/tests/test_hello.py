def test_hello(cli):
    cli.src('hello.c', r"""\
        #include <stdio.h>

        int main() {
            printf("Hello, World!\n");
            return 0;
        }""")

    cli.run('make hello')
    r = cli.run('./hello')

    assert r.out == 'Hello, World!\n'
