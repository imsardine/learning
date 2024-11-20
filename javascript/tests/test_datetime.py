from .conftest import lines

def test_now(workspace):
    r = workspace.eval('''
    const now = Date.now(); // now, timestamp
    const date = new Date(); // Date obj, now

    console.log(typeof now, typeof date);
    console.log(now == date.getTime());
    ''')

    assert r.out == lines(['number object', 'true'])
