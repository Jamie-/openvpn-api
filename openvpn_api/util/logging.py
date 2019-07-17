import sys
import logging

def enable_debug_log():
    """Log output of loggers to stdout for development.
    """
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    root.addHandler(handler)
