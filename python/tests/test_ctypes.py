from ctypes import CDLL, sizeof, create_string_buffer

def test_hello_world(workspace):
    workspace.src('greeting.c', r"""
    #include <stdio.h>

    void greet(char *somebody) {
        printf("Hello, %s!\n", somebody);
    }
    """)

    workspace.src('hello.py', r"""
    import ctypes

    lib = ctypes.CDLL('./greeting.so') # leading ./ is required
    lib.greet(b'World')
    """)

    # -fPIC: Position Independent Code, -shared: shared object (so)
    workspace.run('gcc -fPIC -shared -o greeting.so greeting.c')

    r = workspace.run('python hello.py')
    assert r.out == 'Hello, World!'

def test_mutable_buffer(workspace):
    workspace.src('mylib.c', r"""\
    #include <ctype.h>

    void upper(char *chars, int len) {
      for (int i = 0; i <= len; i++)
        *(chars + i) = toupper(*(chars + i));
    }
    """)

    workspace.run('gcc -fPIC -shared -o mylib.so mylib.c')

    chars = b'abc123'
    buffer = create_string_buffer(chars)

    assert sizeof(buffer) == 7 # len(chars) + 1 (NUL-terminated)
    assert buffer.raw == b'abc123\x00' # raw: memory block content
    assert buffer.value == b'abc123'   # value: as NUL-terminated string

    lib = CDLL('./mylib.so')
    lib.upper(buffer, len(chars))

    assert buffer.value == b'ABC123' # changed in-place
    assert chars == b'abc123' # unchanged
