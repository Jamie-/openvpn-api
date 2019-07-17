# Add submodules for easy access
from . import logging


def nonify_string(string):
    """Return stripped string unless string is empty string, then return None.
    """
    if string is None:
        return None
    string = str(string).strip()
    if len(string) == 0:
        return None
    return string

def nonify_int(string):
    """Return int if string is parsable unless string is empty, then return None."""
    string = nonify_string(string)
    if string is None:
        return string
    return int(string)
