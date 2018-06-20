def test_include(shell):
    shell.src('Makefile', r"""
    include settings

    target:
    	@echo -n $(USERNAME) / $(PASSWORD)
    """)

    shell.src('settings', r"""
    USERNAME = user@example.com
    PASSWORD = secret
    """)

    assert shell.run('make').out == 'user@example.com / secret'

def test_include__file_not_exist__error(shell):
    shell.src('Makefile', r"""
    include settings
    """)

    r = shell.run_err('make')
    assert 'Makefile:1: settings: No such file or directory' in r.err

def test_optional_include__override_from_command_line(shell):
    shell.src('Makefile', r"""
    -include settings

    target:
    	@echo -n $(USERNAME) / $(PASSWORD)
    """)

    shell.src('settings', r"""
    USERNAME ?= user@example.com
    PASSWORD ?= secret
    """)

    assert shell.run('make').out == 'user@example.com / secret'
    assert shell.run('PASSWORD=override make').out == 'user@example.com / override'

