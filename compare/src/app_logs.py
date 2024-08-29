from functools import wraps
from flask import request, current_app
import logging
import os

def log_route(func):
    """
    Decorator that logs the access and completion of a Flask route function.

    This decorator logs the calling and completion of the wrapped function, including the
    function's module and name, the URL rule of the request, and the HTTP method used.

    Args:
        func (function): The Flask route function to be decorated.

    Returns:
        function: The decorated function with logging capability.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Include the name of the function and its module in the log message
        log_message_prefix = f"{func.__module__}.{func.__name__}"

        current_app.logger.info(f"{log_message_prefix}: Route {request.url_rule} called with method {request.method}")
        result = func(*args, **kwargs)
        current_app.logger.info(f"{log_message_prefix}: Finished handling route {request.url_rule}")
        return result
    return decorated_function


def configure_logger(logger):
    """
    Configures the given logger with a standard format and a log level set from an environment variable.

    The logger is set up with a format including the timestamp, module name, log level, and log message.
    The log level is retrieved from the 'LOG_LEVEL' environment variable, defaulting to 'INFO' if not set.

    Args:
        logger (logging.Logger): The logger object to configure.
    """
    formatter = logging.Formatter('%(asctime)s - %(module)s - %(levelname)s - %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    level = os.getenv('LOG_LEVEL', 'INFO').upper()
    logger.setLevel(getattr(logging, level, logging.INFO))
    if not logger.handlers:
        logger.addHandler(stream_handler)

