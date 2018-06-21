def test_ifndef(shell):
    shell.src('Makefile', """
    ifndef WHO
    WHO = World
    endif

    target:
    	@echo -n 'Hello, $(WHO)!'
    """)

    assert shell.run('make').out == 'Hello, World!'
    assert shell.run('WHO=Make make').out == 'Hello, Make!'

def test_ifdef(shell):
    shell.src('Makefile', """
    ifndef WHO
    WHO = World
    endif

    target:
    ifdef DEBUG
    	@echo '[DEBUG] WHO = $(WHO)'
    endif
    	@echo -n 'Hello, $(WHO)!'
    """)

    assert shell.run('make').out == 'Hello, World!'
    assert shell.run('DEBUG=1 WHO=Make make').out == '[DEBUG] WHO = Make\nHello, Make!'
