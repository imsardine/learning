def test_hello_world(workspace):
    workspace.src('index.js', '''
    console.log('Hello, World!');
    ''')

    r = workspace.run('node index.js')
    assert r.out == 'Hello, World!\n'