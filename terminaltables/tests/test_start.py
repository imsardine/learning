# -*- coding: utf-8 -*-
from __future__ import print_function
from textwrap import dedent
from terminaltables import AsciiTable

def test_hello_world():
    data = [
        ['Greeting', 'To'],
        ['Hello', 'World'],
        [u'哈囉', u'世界'],
    ]

    table = AsciiTable(data)

    assert table.table == dedent(u'''
        +----------+-------+
        | Greeting | To    |
        +----------+-------+
        | Hello    | World |
        | 哈囉     | 世界  |
        +----------+-------+
    ''').strip()