from hello import main
import logging
import pytest

# https://docs.pytest.org/en/latest/logging.html

pytest_version = tuple(map(int, pytest.__version__.split('.')))

def test_logging_tuples(caplog):
    if pytest_version >= (3, 4):
        caplog.set_level(logging.DEBUG) # defaults to WARNING

    logging.info('Before calling app code')
    main.say_hello()

    # list of (logger name, severity, message)
    assert caplog.record_tuples == [
        ('root', logging.INFO, 'Before calling app code'),
        ('hello.main', logging.DEBUG, 'somebody: None')
    ]

def test_logging_records(caplog):
    if pytest_version >= (3, 4):
        caplog.set_level(logging.DEBUG)

    main.say_hello()

    logs = caplog.records # list of logging.LogRecord
    assert len(logs) == 1
    assert logs[0].message == 'somebody: None'

def test_logging_text(caplog):
    if pytest_version >= (3, 4):
        caplog.set_level(logging.DEBUG)

    main.say_hello()
    assert 'somebody: None' in caplog.text # final log text

def test_logging_reset(caplog):
    if pytest_version >= (3, 4):
        caplog.set_level(logging.DEBUG)

    logging.info('Before calling app code')
    caplog.clear() # reset captured log records
    main.say_hello()

    assert caplog.record_tuples == [
        ('hello.main', logging.DEBUG, 'somebody: None')
    ]

