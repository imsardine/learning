import re
import requests

def test_hello_world(workspace):
    workspace.src('hello.py', """
    def app(environ, start_response):
        data = b'Hello, World!'
        start_response('200 OK', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(data))),
        ])

        return iter([data])
    """)

    with workspace.spawn('gunicorn -w 4 hello:app') as p:
        p.expect_exact('[INFO] Listening at: http://127.0.0.1:8000')
        p.expect_exact('[INFO] Using worker: sync')

        pids = []
        while True:
            try:
                p.expect(r'\[INFO\] Booting worker with pid: (?P<pid>\d+)\n')
                pids.append(p.match.group('pid'))
            except: # EOF or TIMEOUT
                break

        assert len(pids) == 4 # 4 pre-fork workers (-w 4)
        p.expect_no_more_output()

        resp = requests.get('http://localhost:8000')
        assert resp.text == 'Hello, World!'

