from .conftest import lines

def test_hello_world(workspace):
    workspace.src('hello.ts', '''
    // Say hello to the world
    console.log("Hello TypeScript (TS)!");
    ''')

    # Compile TypeScript (.ts) into JavaScript (.js)
    r = workspace.run('tsc hello.ts')
    assert r.out == ''
    assert workspace.read_txt('hello.js', 'utf-8') == lines('''
    // Say hello to the world
    console.log("Hello TypeScript (TS)!");
    ''')

    # Run the generated JavaScript
    r = workspace.run('node hello.js')
    assert r.out == 'Hello TypeScript (TS)!'
