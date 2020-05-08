import abc


class VPNModel(abc.ABC):
    """Base instance of all VPN data models with parsers."""

    @classmethod
    @abc.abstractmethod
    def parse_raw(cls, raw: str):
        """The parsing method which takes the raw output from the OpenVPN mangement interface and returns an instance of
        the model.
        """
        raise NotImplementedError
