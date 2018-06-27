from hello import say_hello

def test_hello(capsys):
    say_hello('tox')
    out, _ = capsys.readouterr()
    assert out == 'Hello, tox!\n'