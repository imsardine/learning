def test_definition_after_usage__cause_compilation_error(shell):
    shell.src('main.c', r"""
    #include <stdio.h>

    int main() {
        say_hello();
        return 0;
    }

    void say_hello() {
        printf("Hello, World!\n");
    }
    """)

    err = shell.run_err('make main').err
    assert "main.c:4:5: warning: implicit declaration of function 'say_hello' " \
        "is invalid in C99 [-Wimplicit-function-declaration]" in err
    assert "main.c:8:6: error: conflicting types for 'say_hello'" in err

def test_definition_before_usage__passed(shell):
    shell.src('main.c', r"""
    #include <stdio.h>

    void say_hello() {
        printf("Hello, World!\n");
    }

    int main() {
        say_hello();
        return 0;
    }
    """)

    shell.run('make main')
    assert shell.run('./main').out == 'Hello, World!\n'