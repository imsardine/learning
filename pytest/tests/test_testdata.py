from textwrap import dedent

def test_testdata_read(testdata):
    assert testdata.read('data/hello.json') == dedent("""\
        {
          "greeting": "Hello",
          "object": "World"
        }\n""") # why the trailing space?

def test_testdata_json(testdata):
    assert testdata.json('data/hello.json') == {
        'greeting': 'Hello',
        'object': 'World'
    }

