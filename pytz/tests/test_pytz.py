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

def test_convert_timezone():
    dt_utc = datetime(2018, 1, 1, 12, 30 ,45, tzinfo=pytz.utc)
    tz_tpe = pytz.timezone('Asia/Taipei')
    dt_tpe = dt_utc.astimezone(tz_tpe)

    assert dt_tpe.tzinfo.tzname(None) == 'Asia/Taipei'
    assert dt_tpe.replace(tzinfo=None) == datetime(2018, 1, 1, 20, 30, 45)
