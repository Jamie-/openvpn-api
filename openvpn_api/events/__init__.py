import importlib
import typing

from openvpn_api.events import client

event_types = [importlib.import_module(".client", __name__)]


def raise_event(event: typing.Type) -> None:
    raise NotImplementedError
