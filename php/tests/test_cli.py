def test_sapi__cli(workspace):
    assert workspace.run("php -r 'echo php_sapi_name();'").out == 'cli'
    assert workspace.run("php -r 'echo PHP_SAPI;'").out == 'cli'
