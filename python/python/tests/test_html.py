# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
from textwrap import dedent

def test_htmlparser():
    html = dedent("""\
        <html>
          <meta name='author' content="傑洛米高">
          <meta name='description' content="&lt;HTML&gt;" />
        <html>""")

    parser = HTMLMetaParser()
    parser.feed(html.decode('utf-8'))

    assert parser.entries == {
        'author': u'傑洛米高',
        'description': '<HTML>', # no entity refs
    }

class HTMLMetaParser(HTMLParser):

    def __init__(self):
        HTMLParser.__init__(self)
        self.entries = {}

    def handle_starttag(self, tag, attrs):
        if tag != 'meta':
            return

        attrs = dict(attrs)
        if not ('name' in attrs and 'content' in attrs):
            return

        self.entries[attrs['name']] = attrs['content']
