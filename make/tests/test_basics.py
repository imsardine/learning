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

