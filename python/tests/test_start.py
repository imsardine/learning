def test_hello_world(workspace):
    r = workspace.eval('''
    lang = 'Python'
    print(f'Hello, {lang}!') # f-string
    ''')

    assert r.out == 'Hello, Python!'
