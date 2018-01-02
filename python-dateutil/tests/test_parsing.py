from datetime import timedelta, datetime
from dateutil import parser
from dateutil.tz import tzutc

def test_iso_8601_utc():
    dt = parser.parse('2015-08-07T13:50:22.987448Z')
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond) == \
            (2015, 8, 7, 13, 50, 22, 987448)
    assert dt.tzinfo.utcoffset(dt) == timedelta(0)

def test_iso_8600_offset():
    dt = parser.parse('1994-11-05T08:15:30-05:00')
    assert (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second, dt.microsecond) == \
            (1994, 11, 5, 8, 15, 30, 0)
    assert dt.tzinfo.utcoffset(dt) == timedelta(hours=-5)

def test_iso_8600_convert_utc():
    dt = parser.parse('1994-11-05T08:15:30-05:00')
    naive_utc = dt.astimezone(tzutc()).replace(tzinfo=None)

    assert naive_utc.tzinfo is None
    assert naive_utc == datetime(1994, 11, 5, 13, 15, 30, 0)

