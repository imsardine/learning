from hello import main
import logging

# https://docs.pytest.org/en/latest/logging.html

def test_logging_tuples(caplog):
    logging.info('Before calling app code')
    main.say_hello()

    # list of (logger name, severity, message)
    assert caplog.record_tuples == [
        ('root', logging.INFO, 'Before calling app code'),
        ('hello.main', logging.DEBUG, 'somebody: None')
    ]

def test_logging_records(caplog):
    main.say_hello()

    logs = caplog.records # list of logging.LogRecord
    assert len(logs) == 1
    assert logs[0].message == 'somebody: None'

def test_logging_text(caplog):
    main.say_hello()
    assert 'somebody: None' in caplog.text # final log text

def test_logging_reset(caplog):
    logging.info('Before calling app code')
    caplog.clear() # reset captured log records
    main.say_hello()

    assert caplog.record_tuples == [
        ('hello.main', logging.DEBUG, 'somebody: None')
    ]

