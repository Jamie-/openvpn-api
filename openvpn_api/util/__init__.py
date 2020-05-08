from typing import Optional
import netaddr

# Add submodules for easy access
from openvpn_api.util import logging


def nonify_string(string) -> Optional[str]:
    """Return stripped string unless string is empty string, then return None.
    """
    if string is None:
        return None
    string = str(string).strip()
    if len(string) == 0:
        return None
    return string


def nonify_int(string) -> Optional[int]:
    """Return int if string is parsable unless string is empty, then return None."""
    string = nonify_string(string)
    if string is None:
        return string
    return int(string)


def nonify_ip(string) -> Optional[netaddr.IPAddress]:
    """Return netaddr.IPAddress unless string is empty, then return None."""
    string = nonify_string(string)
    if string is None:
        return string
    return netaddr.IPAddress(string)
