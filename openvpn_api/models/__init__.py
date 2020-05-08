import abc
from typing import Optional

import netaddr  # type: ignore


class VPNModelBase(abc.ABC):
    """Base instance of all VPN data models with parsers."""

    @classmethod
    @abc.abstractmethod
    def parse_raw(cls, raw: str):
        """The parsing method which takes the raw output from the OpenVPN management interface and returns an instance
        of the model.
        """
        raise NotImplementedError

    @staticmethod
    def _parse_string(raw: Optional[str]) -> Optional[str]:
        """Return stripped raw unless string is empty raw, then return None.
        """
        if raw is None:
            return None
        raw = str(raw).strip()
        if len(raw) == 0:
            return None
        return raw

    @classmethod
    def _parse_int(self, raw: Optional[str]) -> Optional[int]:
        """Return int if raw is parsable unless raw is empty, then return None."""
        raw = self._parse_string(raw)
        if raw is None:
            return raw
        return int(raw)

    @classmethod
    def _parse_ipv4(cls, raw: Optional[str]) -> Optional[netaddr.IPAddress]:
        """Return netaddr.IPAddress unless raw is empty, then return None."""
        raw = cls._parse_string(raw)
        if raw is None:
            return raw
        return netaddr.IPAddress(raw)
