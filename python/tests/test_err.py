def test_try_finally__for_cleanup_regardless_exc(workspace):
    r1 = workspace.eval('''
    try:
        pass
    finally:
        print('finally')
    ''')

    assert r1.out == 'finally'

    r2 = workspace.eval_err('''
    try:
        1 / 0 # ZeroDivisionError
    finally:
        print('finally') # also executed, even the error
    ''')

    assert r2.out == 'finally'
    assert 'ZeroDivisionError' in r2.err
