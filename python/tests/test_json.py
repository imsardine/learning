# -*- coding: utf-8 -*-
import json
from textwrap import dedent

def test_jsonline_write(workspace):
    workspace.src('data.jsonl', """
    {"entry1": ["value1", "value2"]}
    """)

    new_entry = {"entry2": u"第一行\n第二行"}

    with open('data.jsonl', 'ab') as f:
        line = json.dumps(new_entry, separators=(',', ':'), ensure_ascii=False)
        f.write(b'\n' + line.encode('utf-8')) # leading newline char

    assert open('data.jsonl', 'rb').read().decode('utf-8') == dedent(u"""\
    {"entry1": ["value1", "value2"]}
    {"entry2":"第一行\\n第二行"}""")

def test_jsonline_read(workspace):
    workspace.src('data.jsonl', u"""
    {"entry1": ["value1", "value2"]}
    {"entry2":"第一行\\n第二行"}
    """)

    entries = []
    with open('data.jsonl', 'rb') as f:
        for line in f:
            entry = json.loads(line) # UTF-8 encoding, by default
            entries.append(entry)
    assert entries == [
        {"entry1": ["value1", "value2"]},
        {"entry2": u"第一行\n第二行"},
    ]