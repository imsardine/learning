from .conftest import lines

def test_parse(workspace):
    r = workspace.eval('''
    const json = '{"lang": {"name": "JavaScript", "abbrev": "JS"}, "primitives": [1, true, "str", null]}';
    const obj = JSON.parse(json);
    console.log(obj);
    ''')

    assert r.out == lines('''
    {
      lang: { name: 'JavaScript', abbrev: 'JS' },
      primitives: [ 1, true, 'str', null ]
    }
    ''')

def test_stringify(workspace):
    r = workspace.eval('''
    const obj = {
      lang: { name: 'JavaScript', abbrev: 'JS' },
      primitives: [ 1, true, 'str', null ]
    };

    json = JSON.stringify(obj);
    console.log(json);
    ''')

    assert r.out == '{"lang":{"name":"JavaScript","abbrev":"JS"},"primitives":[1,true,"str",null]}'

def test_formatted_and_reload(workspace):
    r = workspace.eval('''
    const obj = {
      lang: { name: 'JavaScript', abbrev: 'JS' },
      primitives: [ 1, true, 'str', null ]
    };

    json = JSON.stringify(obj);
    objReloaded = JSON.parse(json)
    console.log(obj);
    ''')

    assert r.out == lines('''
    {
      lang: { name: 'JavaScript', abbrev: 'JS' },
      primitives: [ 1, true, 'str', null ]
    }
    ''')

