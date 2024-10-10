from .conftest import lines

def test_object_literal__empty(workspace):
    r = workspace.eval('''
    const obj = {} // empty
    console.log(typeof obj)
    ''')

    assert r.out == 'object'

def test_object_literal__key_numeric_or_valid_identifier_or_quoted(workspace):
    r = workspace.eval('''
    const obj = {
      lang: 'JavaScript', // quotes are optional
      4: 'u', // numeric
      for: 'you',  // even reserved word
      '3rdParty': false // invalid identifier should be quoted (as string literal)
    }

    console.log(`lang: ${ obj.lang }, 4: ${ obj[4] }, for: ${ obj.for }, 3rdParty: ${ obj['3rdParty'] }`)
    ''')

    assert r.out == 'lang: JavaScript, 4: u, for: you, 3rdParty: false'

def test_object_literal__key_invalid_identifier_not_quoted__syntax_error(workspace):
    r = workspace.eval_err('''
    const obj = { 3rdParty: false }
    ''')

    assert 'SyntaxError: Invalid or unexpected token' in r.err

def test_property_access__key_valid_identifier__dot_or_bracket_notation(workspace):
    r = workspace.eval('''
    const obj = { lang: 'JS' }
    const key = 'lang' // via variable, dynamic
    console.log(`obj.lang --> ${ obj.lang }, obj[key] --> ${ obj[key] }`)
    ''')

    assert r.out == 'obj.lang --> JS, obj[key] --> JS'

def test_property_access__key_invalid_identifier__bracket_notation_or_error(workspace):
    r1 = workspace.eval_err('''
    const obj = { '3rdParty': false }
    console.log(obj.3rdParty)
    ''')

    r2 = workspace.eval('''
    const obj = { '3rdParty': false }
    console.log(`obj['3rdParty'] --> ${ obj['3rdParty'] }`)
    ''')

    assert 'SyntaxError: missing ) after argument list' in r1.err # but weird
    assert r2.out == "obj['3rdParty'] --> false"

def test_property_access__key_numeric__bracket_notation_or_error(workspace):
    r1 = workspace.eval_err('''
    const obj = { 3: 'three' }
    console.log(obj.3)
    ''')

    r2 = workspace.eval('''
    const obj = { 3: 'three' }
    console.log(`obj[3] --> ${ obj[3] }, obj['3'] --> ${ obj['3'] }`)
    ''')

    assert 'SyntaxError: missing ) after argument list' in r1.err # but weird
    assert r2.out == "obj[3] --> three, obj['3'] --> three"

def test_object_literal__nested(workspace):
    r = workspace.eval('''
    const lang = {
      name: {
        full: 'JavaScript',
        abbrev: 'JS',
        4: 'u'
      },
    }
    console.log(`${ lang['name'].full } (${ lang.name['abbrev'] }), for ${ lang.name[4] }`)
    ''')

    assert r.out == 'JavaScript (JS), for u'
