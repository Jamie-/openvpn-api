import abc
from typing import Optional, Tuple, Union

from openvpn_api import constants


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
    def _parse_notification(line: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse an OpenVPN real-time notification message into type and message."""
        if line.startswith(">"):
            message = line[1:].split(":", 1)
            assert len(message) == 2, "Malformed notification"
            if message[0] in constants._NOTIFICATION_PREFIXES:
                return message[0], message[1]
        return None, None

    @classmethod
    def _is_notification(cls, line: str) -> bool:
        """Test if `line` is an OpenVPN notification message."""
        notification, message = cls._parse_notification(line)
        return notification is not None and message is not None
