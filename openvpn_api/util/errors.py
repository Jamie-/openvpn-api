class VPNError(Exception):
    """Base exception for all other project exceptions."""


class NotConnectedError(VPNError):
    """Exception raised if not connected to the management interface and a command is called."""


class ConnectError(VPNError):
    """Exception raised on connection failure."""


class ParseError(VPNError):
    """Exception for all management interface parsing errors."""
