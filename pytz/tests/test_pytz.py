from datetime import timedelta
from datetime import datetime
import pytz

REF_DT = datetime(2018, 1, 1, 12, 30, 45)

def test_utc_timezone():
    tz = pytz.utc
    assert tz.utcoffset(REF_DT) == timedelta(0)
    assert tz.dst(REF_DT) == timedelta(0)

def test_taipei_timezone():
    tz = pytz.timezone('Asia/Taipei')
    dt = datetime.now()
    assert tz.utcoffset(REF_DT) == timedelta(hours=8) # UTC+8
    assert tz.dst(REF_DT) == timedelta(0) # DTS is not in effect

