def test_argv0__run_with_python__argv0_is_script_name(workspace):
    workspace.src('run.py', '''
    import sys

    print(type(sys.argv))
    print(sys.orig_argv[0]) # python
    print(sys.argv[0]) # run.py. without the exectuable 'python'
    ''')

    r = workspace.run('python run.py')
    assert r.out == "<class 'list'>\npython\nrun.py"

def test_argv0__with_shebang__argv0_is_script_name(workspace):
    workspace.src('run', '''
    #!/usr/bin/env python
    import sys

    print(sys.orig_argv[0]) # python
    print(sys.argv[0]) # ./run.
    ''')
    workspace.run('chmod a+x run')

    assert workspace.run('./run').out == 'python\n./run'

def test_argv__variable_shell_expansions_performed(workspace):
    workspace.src('filename with spaces.txt')
    workspace.src('run it.py', '''
    import sys
    print(sys.argv)
    ''')

    r = workspace.run(r'''
    VAR1='$HOME in single quotes' && VAR2="$HOME in double quotes" && \
    python run\ it.py --var1 "$VAR1" --var2="$VAR2" -f ~/.bashrc *
    ''')
    assert r.out == \
        "['run it.py', '--var1', '$HOME in single quotes', " \
        "'--var2=/root in double quotes', '-f', '/root/.bashrc', " \
        "'filename with spaces.txt', 'run it.py']"
