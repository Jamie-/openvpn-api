
class VPNError(Exception):
    """Base exception for all other project exceptions.
    """
    pass


class ConnectError(VPNError):
    """Exception raised on connection failure.
    """
    pass


class ParseError(VPNError):
    """Exception for all management interface parsing errors.
    """
    pass
