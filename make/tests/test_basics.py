def test_include(cli):
    cli.src('Makefile', r"""
    include settings

    target:
    	@echo -n $(USERNAME) / $(PASSWORD)
    """)

    cli.src('settings', r"""
    USERNAME = user@example.com
    PASSWORD = secret
    """)

    assert cli.run('make').out == 'user@example.com / secret'

def test_include__file_not_exist__error(cli):
    cli.src('Makefile', r"""
    include settings
    """)

    r = cli.run_err('make')
    assert 'Makefile:1: settings: No such file or directory' in r.err

def test_optional_include__override_from_command_line(cli):
    cli.src('Makefile', r"""
    -include settings

    target:
    	@echo -n $(USERNAME) / $(PASSWORD)
    """)

    cli.src('settings', r"""
    USERNAME ?= user@example.com
    PASSWORD ?= secret
    """)

    assert cli.run('make').out == 'user@example.com / secret'
    assert cli.run('PASSWORD=override make').out == 'user@example.com / override'

