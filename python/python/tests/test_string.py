def test_literal_long():
    s = "part 1" \
        ", part 2" \
        ", part 3"
    assert s == 'part 1, part 2, part 3'

def test_literal_multiline():
    s = """\
line 1
line 2
line 3"""
    assert s == "line 1\nline 2\nline 3"

def test_literal_multiline_dedent():
    from textwrap import dedent
    s = dedent("""\
        line 1
        line 2
        line 3""")
    assert s == "line 1\nline 2\nline 3"

