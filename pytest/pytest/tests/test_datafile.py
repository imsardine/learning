from textwrap import dedent

def test_datafile__read(datafile):
    assert datafile.read('data/hello.json') == dedent("""\
        {
          "greeting": "Hello",
          "object": "World"
        }\n""") # why the trailing space?

def test_datafile_json(datafile):
    assert datafile.json('data/hello.json') == {
        'greeting': 'Hello',
        'object': 'World'
    }

