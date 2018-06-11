from datetime import datetime

class LogRecord:

    def __init__(self, time, level, message):
        self._time = time
        self._level = level
        self._message = message

    @property
    def time(self):
        return self._time

    @property
    def level(self):
        return self._level

    @property
    def message(self):
        return self._message

class LogRecordBuilder():

    def __init__(self):
        self._time = datetime.now()
        self._level = 'DEBUG'
        self._message = 'bla bla bla ...'

    def time(self, time):
        self._time = time
        return self

    def level(self, level):
        self._level = level
        return self

    def message(self, message):
        self._message = message
        return self

    def build(self):
        return LogRecord(self._time, self._level, self._message)

def test_builder_for_testing():
    record = LogRecordBuilder().time(datetime(2014, 9, 1)).level('WARNING').build()
    assert record.time.year == 2014
    assert record.level == 'WARNING'

