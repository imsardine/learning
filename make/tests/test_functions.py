def test_user_defined_function(shell):
    shell.src('Makefile', """
    define hello
    	@echo -n 'Hello,$(1)!'
    endef

    target:
    	$(call hello, World)
    """)

    assert shell.run('make').out == 'Hello, World!'

def test_user_defined_function__whitespaces_between_args_matter(shell):
    shell.src('Makefile', """
    define echo
    	@echo -n '[$(1)]' '[$(2)]' '[$(3)]'
    endef

    target:
    	$(call echo, a, b,c)
    """)

    assert shell.run('make').out == '[ a] [ b] [c]'