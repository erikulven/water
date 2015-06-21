"""Proxy objects for intercepting object acess."""

import time
from contextlib import contextmanager

import settings


logger = settings.getLogger(__name__)


@contextmanager
def log_time(title):
    """
    logs time consumed by operation
    with log_time('PUT stuff'):
        do the stuff
    """
    t1 = time.time()
    yield
    t2 = time.time()
    logger.info("%s took: %0.2f sec", title, t2 - t1)


def time_logger(func):

    def inner(*args, **kwargs):
        with log_time("Call %s(%s, %s)" % (func.__name__, args, kwargs)):
            return func(*args, **kwargs)

    return inner
