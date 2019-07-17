
class VPNError(Exception):
    """Base exception for all other project exceptions.
    """
    pass


class ParseError(VPNError):
    """Exception for all management interface parsing errors.
    """
    pass
