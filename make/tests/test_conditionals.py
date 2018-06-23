def test_ifeq__parentheses__whitespaces_between_args_not_matter(shell):
    makefile =  """
    VAR = value

    target:
    	$(info VAR = [$(VAR)])
    ifeq ($(VAR)%(arg2)s)
    	@echo -n '[$(VAR)] == [value]'
    else
    	@echo -n '[$(VAR)] != [ value]'
    endif
    """

    # preferred, to be consistent with quoted edition and function calls
    shell.src('Makefile', makefile % {'arg2': ',value'})
    assert shell.run('make').out == 'VAR = [value]\n[value] == [value]'

    shell.src('Makefile', makefile % {'arg2': ' , value'})
    assert shell.run('make').out == 'VAR = [value]\n[value] == [value]'

def test_ifeq__quotes__whitespaces_in_quotes_matter(shell):
    makefile = """
    VAR = value

    target:
    	$(info VAR = [$(VAR)])
    ifeq '$(VAR)'%(arg2)s
    	@echo -n '[$(VAR)] == [value]'
    else
    	@echo -n '[$(VAR)] != [ value]'
    endif
    """

    # whitespaces outside of arguments do not matter
    shell.src('Makefile', makefile % {'arg2': "  'value'"})
    assert shell.run('make').out == 'VAR = [value]\n[value] == [value]'

    # whitespaces in arguemnts do matter
    shell.src('Makefile', makefile % {'arg2': "  ' value'"})
    assert shell.run('make').out == 'VAR = [value]\n[value] != [ value]'

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
