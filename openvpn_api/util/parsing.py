from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import Optional, Union

IPAddress = Union[IPv4Address, IPv6Address]


def parse_string(raw: Optional[str]) -> Optional[str]:
    """Return stripped raw unless string is empty raw, then return None.
    """
    if raw is None:
        return None
    raw = str(raw).strip()
    if len(raw) == 0:
        return None
    return raw


def parse_int(raw: Optional[str]) -> Optional[int]:
    """Return int if raw is parsable unless raw is empty, then return None."""
    raw = parse_string(raw)
    if raw is None:
        return raw
    return int(raw)


def parse_ipaddress(raw: Optional[str]) -> Optional[IPAddress]:
    """Return IPAddress unless raw is empty, then return None."""
    raw = parse_string(raw)
    if raw is None:
        return None
    return ip_address(raw)
