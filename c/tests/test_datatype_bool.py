def test_comparison_result__zero_for_false_and_one_for_true(shell):
    shell.src('test.c', r"""
    #include <stdio.h>

    int main() {
        printf("3 > 2 => %d", 3 > 2);
        printf("2 > 3 => %d", 2 > 3);
    }
    """)

    shell.run('make test')
    r = shell.run('./test')

    assert r.out == '3 > 2 => 1' \
                    '2 > 3 => 0'

def test_conditional_testing__zero_for_false_and_non_zero_for_true(shell):
    shell.src('test.c', r"""
    #include <stdio.h>

    int main() {
        if (3) {
            printf("non-zero is considered as true");
        } else {
            printf("BOOM!");
        }

        if (0) {
            printf("BOOM!");
        } else {
            printf("zero is considered as false");
        }
    }
    """)

    shell.run('make test')
    r = shell.run('./test')

    assert r.out == 'non-zero is considered as true' \
                    'zero is considered as false'

def test_logical_operator__zero_for_false_and_non_zero_for_true(shell):
    shell.src('test.c', r"""
    #include <stdio.h>

    int main() {
        printf("3 > 2 && 4 > 3 => %d", 3 > 2 && 4 > 3);
        printf("3 > 2 && 3 > 4 => %d", 3 > 2 && 3 > 4);
        printf("2 && 3 => %d", 2 && 3);
        printf("2 && 0 => %d", 2 && 0);
        printf("-1 && 1 => %d", -1 && 1);
    }
    """)

    shell.run('make test')
    r = shell.run('./test')

    assert r.out == '3 > 2 && 4 > 3 => 1' \
                    '3 > 2 && 3 > 4 => 0' \
                    '2 && 3 => 1'         \
                    '2 && 0 => 0'         \
                    '-1 && 1 => 1'

def test_assignment__assignment_has_a_value(shell):
    shell.src('test.c', r"""
    #include <stdio.h>

    int main() {
        int x = 1;
        if (x = x - 1) { // --x
            printf("BOOM!");
        } else {
            printf("x (%d) is considered false", x);
        }

        if (--x) {
            printf("x (%d) is considered true", x);
        } else {
            printf("BOOM!");
        }
    }
    """)

    shell.run('make test')
    r = shell.run('./test')

    assert r.out == 'x (0) is considered false' \
                    'x (-1) is considered true'

def test_c99_bool__true_false_constants_can_be_used_as_integers(shell):
    shell.src('test.c', r"""
    #include <stdio.h>
    #include <stdbool.h>

    int main() {
        printf("true => %d, false => %d", true, false);

        bool true_equals_to_one = true == 1;
        printf("true == 1 => %d", true_equals_to_one);

        bool true_equals_to_zero = false == 0;
        printf("false == 0 => %d", true_equals_to_zero);
    }
    """)

    shell.run('make test')
    r = shell.run('./test')

    assert r.out == 'true => 1, false => 0' \
                    'true == 1 => 1'        \
                    'false == 0 => 1'
