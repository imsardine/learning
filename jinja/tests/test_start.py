from jinja2 import Template

def test_hello_world(py2):
    template = Template('Hello, {{ name }}!')
    context = {'name': 'World'}

    out = template.render(context)

    unicode_type = unicode if py2 else str
    assert out == 'Hello, World!'
    assert type(out) == unicode_type