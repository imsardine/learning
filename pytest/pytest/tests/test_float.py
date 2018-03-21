from pytest import approx

def test_simple_equal__not_working():
    assert not 1.0 / 7 == 0.142857142857

def test_almost_equal__approx():
    assert repr(approx(0.5, rel=1e-3)) == '0.5 +- 5.0e-04'
    assert repr(approx(0.5, abs=1e-3)) == '0.5 +- 1.0e-03'

    assert 1.0 / 7 == approx(0.142857142857) # rel=1e-6, abs=1e-12
    assert 1.0 / 7 == approx(0.1428, abs=1e-4) # 0.1427 ... 0.1429

def test_almost_equal__scale():
    assert int((1.0 / 7) * 10**4) == 1428 # 0.1428... x 10000 = 1428...
