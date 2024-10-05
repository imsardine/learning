def test_multiline__array_join(workspace):
    workspace.src('index.js', r'''
    var lines = [
      'line1',
      'line2'
    ].join('\n')
    console.log('[' + lines + ']')
    ''')

    r = workspace.run('node index.js')
    assert r.out == '[line1\nline2]'

def test_multiline__string_concatenation(workspace):
    workspace.src('index.js', r'''
    var lines =
      'line1\n' +
      'line2'
    console.log('[' + lines + ']')
    ''')

    r = workspace.run('node index.js')
    assert r.out == '[line1\nline2]'

def test_multiline__template_literal__may_not_work(workspace):
    workspace.src('index.js', r'''
    var lines =
      `line1
      line2`
    console.log('[' + lines + ']')
    ''')

    # leading whitespaces are preserved
    r = workspace.run('node index.js')
    assert r.out == '[line1\n  line2]'

def test_template_literal__interpolation(workspace):
    workspace.src('index.js', r'''
    var name = 'Jeremy', time = 'today'
    console.log(`Hi ${name}, how are you ${time}?`)
    ''')

    r = workspace.run('node index.js')
    assert r.out == 'Hi Jeremy, how are you today?'
