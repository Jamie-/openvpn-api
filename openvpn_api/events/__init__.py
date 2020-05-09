import importlib
import typing

from openvpn_api.events import client

event_types = [importlib.import_module(".client", __name__)]

_callbacks = []


def raise_event(event: typing.Type) -> None:
    for callback in _callbacks:
        callback(event)


def register_callback(callback: typing.Callable[[typing.Type], typing.Any]) -> None:
    _callbacks.append(callback)
