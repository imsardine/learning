from .matchers import *

TEST_SKIPPING_PY = """
    import pytest

    @pytest.mark.skip(reason='Reason for skipping')
    def test_skip():
        assert False

    @pytest.mark.xfail(reason='Reason for xfailed')
    def test_xfail_xfailed():
        assert False

    @pytest.mark.xfail(reason='Reason for xpassed')
    def test_xfail_xpassed():
        pass
    """

def test_skipping__no_extra_summary__xpass_not_cause_failure(shell):
    shell.src('test_skipping.py', TEST_SKIPPING_PY)

    r = shell.run('pytest -v')
    assert r.out == like("""
    ... collected 3 items

    test_skipping.py::test_skip SKIPPED                                      [ 33%]
    test_skipping.py::test_xfail_xfailed xfail                               [ 66%]
    test_skipping.py::test_xfail_xpassed XPASS                               [100%]

    =============== 1 skipped, 1 xfailed, 1 xpassed in ...
    """)
    assert r.rc == 0

def test_skipping__with_extra_summary__xpass_not_cause_failure(shell):
    shell.src('test_skipping.py', TEST_SKIPPING_PY)

    # -ra, where 'a' stands for (a)ll except passed
    r = shell.run('pytest -v -ra')

    assert r.out == like("""
    ... collected 3 items

    test_skipping.py::test_skip SKIPPED                                      [ 33%]
    test_skipping.py::test_xfail_xfailed xfail                               [ 66%]
    test_skipping.py::test_xfail_xpassed XPASS                               [100%]
    =========================== short test summary info ============================
    SKIP [1] test_skipping.py:3: Reason for skipping
    XFAIL test_skipping.py::test_xfail_xfailed
      Reason for xfailed
    XPASS test_skipping.py::test_xfail_xpassed Reason for xpassed

    =============== 1 skipped, 1 xfailed, 1 xpassed in ...
    """)
    assert r.rc == 0

def test_skipping__enable_strict_option__xpass_cause_failure(shell):
    shell.src('test_skipping.py', TEST_SKIPPING_PY)

    r = shell.run_err('pytest -v -o xfail_strict=true')
    print r.out
    assert r.out == like("""
    ... collected 3 items

    test_skipping.py::test_skip SKIPPED                                      [ 33%]
    test_skipping.py::test_xfail_xfailed xfail                               [ 66%]
    test_skipping.py::test_xfail_xpassed FAILED                              [100%]

    =================================== FAILURES ===================================
    ______________________________ test_xfail_xpassed ______________________________
    [XPASS(strict)] Reason for xpassed
    ================ 1 failed, 1 skipped, 1 xfailed in ...
    """)
    assert r.rc == 1
