"""
Logging module defines 'log_function' decorator
"""

import logging

logger = logging.getLogger(__name__)


# defines a decorator for logging function calls
def log_function(func):
    """Decorator for logging function calls and arguments"""

    def wrapper(*args, **kwargs):
        logger.info(
            "'%s' called with args: '%s' and kwargs: '%s'", func.__name__, args, kwargs
        )
        return func(*args, **kwargs)

    return wrapper
