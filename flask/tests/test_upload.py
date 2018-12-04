import requests
import base64

def test_upload(workspace, testdata):
    workspace.src('upload.py', r"""
    import base64
    from flask import Flask, request, jsonify

    app = Flask(__name__)

    @app.route('/', methods=['POST'])
    def upload():
        files = []
        for name in request.files:
            fs = request.files[name] # werkzeug.datastructures.FileStorage

            # decoding is needed, or TypeError: Object of type 'bytes' is not JSON serializable
            content = base64.standard_b64encode(fs.read()).decode('ascii')

            entry = {
                'name': fs.name,
                'filename': fs.filename,
                'content_length': fs.content_length,
                'content_type': fs.content_type,
                'content': content,
            }
            files.append(entry)

        return jsonify(files)
    """)

    with workspace.spawn('FLASK_APP=upload.py flask run') as p:
        p.expect_exact('Press CTRL+C to quit')

        imgfn = testdata.relpath('data/google.png')
        with open(imgfn, 'rb') as f:
            resp = requests.post('http://localhost:5000', files={'file': ('google-logo.png', f)})

        json = resp.json()
        assert json[0]['name'] == 'file'
        assert json[0]['filename'] == 'google-logo.png'
        assert base64.standard_b64decode(json[0]['content']) == open(imgfn, 'rb').read()
