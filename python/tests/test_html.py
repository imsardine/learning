# -*- coding: utf-8 -*-
import sys
py2 = sys.version_info[0] == 2

if py2:
    from HTMLParser import HTMLParser
else:
    from html.parser import HTMLParser

from textwrap import dedent

def test_htmlparser():
    html = dedent("""\
        <html>
          <meta name='author' content="傑洛米高">
          <meta name='description' content="&lt;HTML&gt;" />
        <html>""")
    if py2:
        html = html.decode('utf-8') # feed(unicode) is advised

    parser = HTMLMetaParser()
    parser.feed(html)

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
