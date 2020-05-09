import importlib
import typing

event_types = []


def raise_event(event: typing.Type) -> None:
    raise NotImplementedError
