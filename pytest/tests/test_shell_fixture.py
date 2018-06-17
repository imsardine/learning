import sys
import requests
import pytest

def test_shell_spawn(shell):
    shell.src('index.html', "<html>Hello, World!</html>")

    http_mod = 'http.server' if sys.version_info[0] >= 3 else 'SimpleHTTPServer'
    with shell.spawn('python -m %s 8000' % http_mod) as p:
        p.expect_exact('Serving HTTP on 0.0.0.0 port 8000')

        resp = requests.get('http://localhost:8000')
        assert resp.text == '<html>Hello, World!</html>'

