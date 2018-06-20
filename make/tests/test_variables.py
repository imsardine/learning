from textwrap import dedent

def test_target_specific_variable(shell):
    shell.src('Makefile', """
    VAR = global

    not-target-specific:
    	@echo -n 'VAR = $(VAR)'

    target-specific: VAR = target-specific
    target-specific:
    	@echo -n 'VAR = $(VAR)'
    """)

    r1 = shell.run('make not-target-specific')
    r2 = shell.run('make target-specific')

    assert r1.out == 'VAR = global'
    assert r2.out == 'VAR = target-specific'

def test_target_specific_variable__multiple(shell):
    shell.src('Makefile', """
    # Even target-specific variables are not predefined

    target: VAR1 = value1
    target: VAR2 = value2
    target:
    	@echo -n 'VAR1 = $(VAR1), VAR2 = $(VAR2)'
    """)

    r = shell.run('make').out == 'VAR1 = value1, VAR2 = value2'

def test_target_specific_variable__conditional_override(shell):
    shell.src('Makefile', """
    target: VAR ?= original
    target:
    	@echo -n 'VAR = $(VAR)'
    """)

    assert shell.run('make').out == 'VAR = original'
    assert shell.run("VAR=changed make").out == 'VAR = changed'

def test_target_specific_variable__in_effect_prerequisites(shell):
    shell.src('Makefile', """
    prerequisite: VAR2 = value2 (custom)
    prerequisite: VAR3 = value3
    prerequisite:
    	@echo 'prerequisite: VAR1 = $(VAR1), VAR2 = $(VAR2), VAR3 = $(VAR3)'

    target: VAR1 = value1
    target: VAR2 = value2
    target: prerequisite
    	@echo 'target: VAR1 = $(VAR1), VAR2 = $(VAR2)'
    """)

    assert shell.run('make target').out == dedent("""\
        prerequisite: VAR1 = value1, VAR2 = value2 (custom), VAR3 = value3
        target: VAR1 = value1, VAR2 = value2
    """)
