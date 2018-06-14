import urllib2

def test_cli_daemon(cli):
    cli.src('index.html', "<html>Hello, World!</html>")

    with cli.run('python -m SimpleHTTPServer 8000') as p:
        # Serving HTTP on 0.0.0.0 port 8000 ...
        import time; time.sleep(2)

        resp = urllib2.urlopen('http://localhost:8000')
        assert resp.read() == '<html>Hello, World!</html>'

