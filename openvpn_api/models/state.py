"""
COMMAND -- state
----------------

Show the current OpenVPN state, show state history, or enable real-time notification of state changes.

These are the OpenVPN states:

CONNECTING    -- OpenVPN's initial state.
WAIT          -- (Client only) Waiting for initial response from server.
AUTH          -- (Client only) Authenticating with server.
GET_CONFIG    -- (Client only) Downloading configuration options from server.
ASSIGN_IP     -- Assigning IP address to virtual network interface.
ADD_ROUTES    -- Adding routes to system.
CONNECTED     -- Initialization Sequence Completed.
RECONNECTING  -- A restart has occurred.
EXITING       -- A graceful exit is in progress.
RESOLVE       -- (Client only) DNS lookup
TCP_CONNECT   -- (Client only) Connecting to TCP server

The output format consists of up to 9 comma-separated parameters:
  (a) the integer unix date/time,
  (b) the state name,
  (c) optional descriptive string (used mostly on RECONNECTING and EXITING to show the reason for the disconnect),
  (d) optional TUN/TAP local IPv4 address
  (e) optional address of remote server,
  (f) optional port of remote server,
  (g) optional local address,
  (h) optional local port, and
  (i) optional TUN/TAP local IPv6 address.
"""


import datetime
from typing import Optional

import netaddr  # type: ignore


class State:
    """OpenVPN daemon state model."""

    def __init__(
        self,
        up_since: Optional[str] = None,
        state_name: Optional[str] = None,
        desc_string: Optional[str] = None,
        local_virtual_v4_addr: Optional[str] = None,
        remote_addr: Optional[str] = None,
        remote_port: Optional[int] = None,
        local_addr: Optional[str] = None,
        local_port: Optional[int] = None,
        local_virtual_v6_addr: Optional[str] = None,
    ) -> None:
        # Datetime daemon started?
        self.up_since = (
            datetime.datetime.utcfromtimestamp(int(up_since)) if up_since else None
        )  # type: datetime.datetime
        # See states list in module docstring
        self.state_name = state_name  # type: str
        self.desc_string = desc_string  # type: str
        self.local_virtual_v4_addr = (
            netaddr.IPAddress(local_virtual_v4_addr) if local_virtual_v4_addr else None
        )  # type: netaddr.IPAddress
        self.remote_addr = remote_addr  # type: str
        self.remote_port = int(remote_port) if remote_port else None  # type: int
        self.local_addr = local_addr  # type: str
        self.local_port = int(local_port) if local_port else None  # type: int
        self.local_virtual_v6_addr = local_virtual_v6_addr  # type: str

    @property
    def mode(self) -> str:
        if self.remote_addr is None and self.local_addr is None:
            return "unknown"
        if self.remote_addr is None:
            return "server"
        return "client"
