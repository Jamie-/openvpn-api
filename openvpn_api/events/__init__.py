import pathlib
import importlib
from typing import List, Type

from openvpn_api.events.base import BaseEvent

# Registered server-transmitted events
_events = []


def register_event(event_type: Type[BaseEvent]) -> Type[BaseEvent]:
    """Register an event handler."""
    if event_type not in _events:
        _events.append(event_type)
    return event_type


def get_event_types() -> List[Type[BaseEvent]]:
    """Get all registered event types."""
    return _events.copy()


# Import all standard events we have so they get registered
for _file in pathlib.Path(__file__).parent.glob("*.py"):
    if _file.name.startswith("_"):
        continue
    importlib.import_module(f"openvpn_api.events.{_file.stem}")
del _file  # Remove _file from module namespace after we're done
