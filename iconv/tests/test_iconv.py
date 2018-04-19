# -*- coding: utf-8 -*-
from os import path

def test_list_supported_encoding(shell):
    out, _, _ = shell('iconv --list')

    lines = out.splitlines()
    assert len(lines) > 100 # lots of encodings
    assert 'UTF-8 UTF8' in lines # alternatives

def test_big5_to_utf8(shell):
    out, _, _ = shell('iconv -f big5 -t utf8 data/big5.txt')
    assert out.decode('utf8') == u'你好嗎?'

def test_utf8_to_big5(shell):
    out, _, _ = shell('iconv -f utf8 -t big5 data/utf8.txt')
    assert out.decode('big5') == u'你好嗎?'

def test_to_file(shell, tmpdir):
    out_file = path.join(tmpdir.strpath, 'big5.txt')

    shell('iconv -f utf8 -t big5 data/utf8.txt > %s' % out_file)

    with open(out_file, 'rb') as f:
        assert f.read().decode('big5') == u'你好嗎?'
