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