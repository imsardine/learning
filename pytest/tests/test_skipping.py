def test_skipping__no_extra_summary(cli):
    r1 = cli.run('pytest -v data/tests/test_skip.py')
    r2 = cli.run('pytest -v data/tests/test_xfail.py')

    assert 'Reason for' not in r1.out
    assert 'Reason for' not in r2.out

def test_skipping__with_extra_summary(cli):
    # -ra, where 'a' stands for (a)ll except passed
    r1 = cli.run('pytest -v -ra data/tests/test_skip.py')
    r2 = cli.run('pytest -v -ra data/tests/test_xfail.py')

    assert 'Reason for skipping' in r1.out
    assert 'Reason for expecting to fail (xfailed)' in r2.out
    assert 'Reason for expecting to fail (xpassed)' in r2.out

def test_skip(cli):
    r = cli.run('pytest -v data/tests/test_skip.py')

    assert '== 1 passed, 1 skipped in ' in r.out
    assert '::test_with_skip_mark__skipped SKIPPED ' in r.out
    assert '::test_without_skip_mark__not_skipped PASSED ' in r.out
    assert r.rc == 0

def test_xfail(cli):
    r = cli.run('pytest -v data/tests/test_xfail.py')

    assert '== 1 passed, 1 xfailed, 1 xpassed in ' in r.out # xpassed != passed
    assert '::test_without_xfail_mark__passed PASSED ' in r.out
    assert '::test_expected_to_fail__failed__xfailed xfail ' in r.out # lower-case
    assert '::test_expected_to_fail__passed__xpassed XPASS ' in r.out
    assert r.rc == 0