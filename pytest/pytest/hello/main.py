import logging

logger = logging.getLogger(__name__)

def say_hello(somebody=None):
    logger.debug('somebody: %r', somebody)
    if not somebody:
        somebody = 'World'
    greeting = 'Hello, %s!' % somebody

    print greeting

