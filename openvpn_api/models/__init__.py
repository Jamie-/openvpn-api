import abc
from typing import Optional

import netaddr  # type: ignore
from openvpn_api import _constants


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

    @staticmethod
    def _parse_notification(line: str) -> (Optional[str], Optional[str]):
        """Parse an OpenVPN real-time notification message into type and message."""
        if line.startswith(">"):
            message = line[1:].split(":", 1)
            assert len(message) == 2, "Malformed notification"
            if message[0] in _constants.NOTIFICATION_PREFIXES:
                return (message[0], message[1])
        return (None, None)

    @classmethod
    def _is_notification(cls, line: str) -> bool:
        """Test if `line` is an OpenVPN notification message."""
        notification, message = cls._parse_notification(line)
        return notification is not None and message is not None
