from textwrap import dedent

def test_datafile__read(datafile):
    assert datafile.read('hello.json') == dedent("""\
        {
          "greeting": "Hello",
          "object": "World"
        }\n""") # why the trailing space?

def test_datafile_json(datafile):
    assert datafile.json('hello.json') == {
        'greeting': 'Hello',
        'object': 'World'
    }

