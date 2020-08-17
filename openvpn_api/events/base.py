import abc
from typing import List


class BaseEvent(abc.ABC):
    """Base class for all server-initiated events."""

    @classmethod
    @abc.abstractmethod
    def has_begun(cls, line: str) -> bool:
        """Check if line matches the first message expected by this event parser."""

    @classmethod
    @abc.abstractmethod
    def has_ended(cls, line: str) -> bool:
        """Check if line matches the final message expected by this event parser."""

    @classmethod
    @abc.abstractmethod
    def parse_raw(cls, lines: List[str]):
        """Parse the gathered lines and return an instance of the event class."""
