from datetime import datetime, date
import json
import pytz
import pytest

def test_date_not_json_serializable():
    dt = date(2018, 1, 2)
    with pytest.raises(TypeError) as excinfo:
        json.dumps(dt)

    assert excinfo.value.message == \
            'datetime.date(2018, 1, 2) is not JSON serializable'

def test_datetime_not_json_serializable():
    dt = datetime(2018, 1, 2, 13, 50)
    with pytest.raises(TypeError) as excinfo:
        json.dumps(dt)

    assert excinfo.value.message == \
            'datetime.datetime(2018, 1, 2, 13, 50) is not JSON serializable'

def test_default_serializer():
    def default(obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        else:
            return str(obj)
            # raise TypeError('%r is not JSON serializable' % obj)

    data = [
        date(2018, 1, 2),
        datetime(2018, 1, 2, 13, 50, tzinfo=pytz.utc),
    ]
    s = json.dumps(data, default=default)
    assert s == '["2018-01-02", "2018-01-02T13:50:00+00:00"]'

