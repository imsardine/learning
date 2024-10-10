from .conftest import lines

def test_literal__single_double_no_difference(workspace):
    r = workspace.eval('''
    const message = 'Keep learning, ' + "don't stop!"
    console.log(message)
    ''')

    assert r.out == "Keep learning, don't stop!"

def test_literal__no_character_type(workspace):
    r = workspace.eval('''
    const char = 'c'
    console.log(`${ typeof char } (${ char.length })`) // string
    ''')

    assert r.out == 'string (1)'

def test_multiline__array_join(workspace):
    r = workspace.eval(r'''
    const lines = [
      'line1',
      'line2'
    ].join('\n')
    console.log(`[${lines}]`)
    ''')

    assert r.out == '[line1\nline2]'

def test_multiline__string_concatenation(workspace):
    r = workspace.eval(r'''
    const lines =
      'line1\n' +
      'line2'
    console.log(`[${lines}]`)
    ''')

    assert r.out == '[line1\nline2]'

def test_multiline__template_literal__may_not_work(workspace):
    r = workspace.eval('''
    const lines =
      `line1
      line2`
    console.log(`[${lines}]`)
    ''')

    # leading whitespaces are preserved
    assert r.out == '[line1\n  line2]'

def test_template_literal__interpolation(workspace):
    r = workspace.eval('''
    const name = 'Jeremy', time = 'today'
    console.log(`Hi ${name}, how are you ${time}?`)
    ''')

    assert r.out == 'Hi Jeremy, how are you today?'

def test_string_concatenation__addition_operator(workspace):
    # https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Addition
    r = workspace.eval('''
    const name = 'Jeremy'
    console.log('Hello, World! Hello ' + name + '!')
    ''')

    assert r.out == 'Hello, World! Hello Jeremy!'

def test_string_concatenation__template_literal(workspace):
    r = workspace.eval('''
    const name = 'Jeremy'
    console.log(`Hello, World! Hello ${name}!`)
    ''')

    assert r.out == 'Hello, World! Hello Jeremy!'

def test_string_concatenation__string_concat(workspace):
    r = workspace.eval('''
    const name = 'Jeremy'
    console.log('Hello, World! Hello '.concat(name).concat('!'))
    ''')

    assert r.out == 'Hello, World! Hello Jeremy!'
