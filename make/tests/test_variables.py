from textwrap import dedent

def test_variable__empty_string(shell):
    shell.src('Makefile', """
    IMPLICIT_EMPTY =
    EXPLICIT_EMPTY = ''

    target:
    	@echo -n
    	$(info Implicit = [$(IMPLICIT_EMPTY)])
    	$(info Explicit = [$(EXPLICIT_EMPTY)])
    """)

    # Value `''` doesn't mean empty string to make itself
    assert shell.run('make').out == "Implicit = []\nExplicit = ['']\n"

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

def test_multiline_variable__implicit_assignment_operator(shell):
    shell.src('Makefile', """
    define VAR
        line 1
      line 2 (indented)
    endef

    target:
    	@echo -n
    	$(info [$(VAR)])
    """)

    # the trailing newline is not part of the value
    assert shell.run('make').out == '[    line 1\n  line 2 (indented)]\n'

def test_multiline_variable__explicit_assignment_operator__unexpected_empty(shell):
    shell.src('Makefile', """
    define VAR =
        line 1
      line 2 (indented)
    endef

    target:
    	@echo -n
    	$(info [$(VAR)])
    """)

    assert shell.run('make').out == '[]\n'

def test_multiline_variable__as_canned_recipes(shell):
    shell.src('Makefile', """
    define COMMANDS
    @echo step 1
    	@echo step 2
    endef

    target:
    	$(COMMANDS)
    """)

    # inconsistent indentation doesn't matter
    assert shell.run('make').out == 'step 1\nstep 2\n'
