
class VPNError(Exception):
    """Base exception for all other project exceptions.
    """
    pass


class InvalidConfigError(VPNError):
    """Invalid config provided.
    """
    pass


class ParseError(VPNError):
    """Exception for all management interface parsing errors.
    """
    pass
