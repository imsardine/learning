def test_include(cli):
    r = cli.run('make', cwd='basics/include')
    assert r.out == 'user@example.com / secret'

