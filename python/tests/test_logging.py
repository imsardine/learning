import time
import logging
import pytest

try:
    import mock
except ImportError:
    from unittest import mock

@pytest.fixture
def output(py2):
    if py2:
        from StringIO import StringIO
    else:
        from io import StringIO

    return StringIO()

@pytest.fixture
def logger(output):
    logger = logging.getLogger(__name__)
    for handler in logger.handlers:
        logger.removeHandler(handler)

    handler = logging.StreamHandler(stream=output)
    logger.addHandler(handler)

    return logger

def test_basicconfig__message_format_string__defaults_level_name_message(workspace):
    workspace.src('test.py', r'''
    import logging

    logging.basicConfig()
    root = logging.getLogger()

    root.warning('log message')
    ''')

    r = workspace.run('python test.py')
    assert r.err == 'WARNING:root:log message' # severity:logger name:message

def test_formatter_message_format_string__defaults_raw_message(logger, output):
    logger.handlers[0].setFormatter(logging.Formatter())
    logger.warning('log message')

    assert output.getvalue() == 'log message\n' # raw message

@mock.patch.object(logging.time, 'time')
def test_formatter_time_zone__defaults_local_time(logging_time_time, logger, output):
    logging_time_time.return_value = 1543714200 # 2018-12-02 09:30 (UTC+8)
    logger.handlers[0].setFormatter(logging.Formatter('%(asctime)s %(message)s'))

    logger.warning('log message')
    assert output.getvalue() == '2018-12-02 09:30:00,000 log message\n'

@mock.patch.object(logging.time, 'time')
def test_formatter_time_zone__use_utc_instead(logging_time_time, logger, output):
    logging_time_time.return_value = 1543714200 # 2018-12-02 09:30 (UTC+8)

    formatter = logging.Formatter('%(asctime)s %(message)s')
    formatter.converter = time.gmtime # defaults to time.localtime
    logger.handlers[0].setFormatter(formatter)

    logger.warning('log message')
    assert output.getvalue() == '2018-12-02 01:30:00,000 log message\n'
