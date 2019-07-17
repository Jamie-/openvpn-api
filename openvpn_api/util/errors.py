
class MonitorError(Exception):
    """Base exception for all other project exceptions.
    """
    pass


class InvalidConfigError(MonitorError):
    """Invalid config provided.
    """
    pass


class ParseError(MonitorError):
    """Exception for all management interface parsing errors.
    """
    pass
