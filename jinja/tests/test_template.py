from jinja2 import Environment, Template

def test_whitespace__default__all_whitespaces_preserved_except_for_trailing_newline():
    env = Environment()
    template = env.from_string('\t {% if True %}\n'
                               '\t content\n'
                               '\t {% endif %}\n')
    assert template.render() == '\t \n' \
                                '\t content\n' \
                                '\t ' # newline at the end is gone

def test_whitespace__trim_blocks_on__trailing_newline_removed():
    env = Environment(trim_blocks=True)
    template = env.from_string('\t {% if True %}\n '
                               '\t content\n'
                               '\t {% endif %}\n\t')

    assert template.render() == '\t  ' \
                                '\t content\n' \
                                '\t \t'

def test_whitespace__trim_blocks_on__only_adjacent_newline_removed():
    env = Environment(trim_blocks=True)
    template = env.from_string('\t {% if True %}\n '  # adjacent -> removed
                               '\t content\n'
                               '\t {% endif %} \n\t') # no adjacent -> preserved

    assert template.render() == '\t  ' \
                                '\t content\n' \
                                '\t  \n\t'

def test_whitespace__lstrip_blocks_on__leading_whitespaces_removed():
    env = Environment(lstrip_blocks=True)
    template = env.from_string('static \n'
                               '\t {% if True %}\n '
                               '\t dynamic\n'
                               '\t {% endif %} \n\t')

    assert template.render() == 'static \n' \
                                '\n ' \
                                '\t dynamic\n' \
                                ' \n\t'

def test_whitespace__both_trim_lstrip_block_on__entire_block_lines_removed(): # general use
    env = Environment(trim_blocks=True, lstrip_blocks=True)
    template = env.from_string('\t {% if True %}\n'
                               '\t content\n'
                               '\t {% endif %}\n')

    assert template.render() == '\t content\n'

def test_whitespace__minus_sign___whitespaces_removed_multilines():
    env = Environment()
    template = env.from_string('static \n'
                               '\t {%- if True %}\n '
                               '\t dynamic\n'
                               '\t {% endif -%} \n\t')

    assert template.render() == 'static' \
                                '\n ' \
                                '\t dynamic\n' \
                                '\t '
