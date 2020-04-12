
class VPNError(Exception):
    """Base exception for all other project exceptions.
    """
    pass


class NotConnectedError(VPNError):
    """Exception raised if not connected to the management interface and a command is called."""
    pass


class ConnectError(VPNError):
    """Exception raised on connection failure.
    """
    pass


class ParseError(VPNError):
    """Exception for all management interface parsing errors.
    """
    pass
