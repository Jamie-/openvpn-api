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

from openvpn_api.models import VPNModelBase
from openvpn_api.util import errors, parsing
from openvpn_api.util.parsing import IPAddress


class State(VPNModelBase):
    """OpenVPN daemon state model."""

    def __init__(
        self,
        up_since: datetime.datetime = None,
        state_name: str = None,
        desc_string: str = None,
        local_virtual_v4_addr: IPAddress = None,
        remote_addr: IPAddress = None,
        remote_port: int = None,
        local_addr: IPAddress = None,
        local_port: int = None,
        local_virtual_v6_addr: str = None,
    ) -> None:
        # Datetime daemon started?
        self.up_since: Optional[datetime.datetime] = up_since
        # See states list in module docstring
        self.state_name: Optional[str] = state_name
        self.desc_string: Optional[str] = desc_string
        self.local_virtual_v4_addr: Optional[IPAddress] = local_virtual_v4_addr
        self.remote_addr: Optional[IPAddress] = remote_addr
        self.remote_port: Optional[int] = remote_port
        self.local_addr: Optional[IPAddress] = local_addr
        self.local_port: Optional[int] = local_port
        self.local_virtual_v6_addr: Optional[str] = local_virtual_v6_addr

    @property
    def mode(self) -> str:
        if self.remote_addr is None and self.local_addr is None:
            return "unknown"
        if self.remote_addr is None:
            return "server"
        return "client"

    @classmethod
    def parse_raw(cls, raw: str) -> "State":
        for line in raw.splitlines():
            if cls._is_notification(line):
                continue
            if line.strip() == "END":
                break
            parts = line.split(",")
            assert len(parts) >= 8, "Received too few parts to parse state."
            # 0 - Unix timestamp of server start (UTC?)
            up_since = datetime.datetime.utcfromtimestamp(int(parts[0])) if parts[0] != "" else None
            # 1 - Connection state
            state_name = parsing.parse_string(parts[1])
            # 2 - Connection state description
            desc_string = parsing.parse_string(parts[2])
            # 3 - TUN/TAP local v4 address
            local_virtual_v4_addr = parsing.parse_ipaddress(parts[3])
            # 4 - Remote server address (client only)
            remote_addr = parsing.parse_ipaddress(parts[4])
            # 5 - Remote server port (client only)
            remote_port = parsing.parse_int(parts[5])
            # 6 - Local address
            local_addr = parsing.parse_ipaddress(parts[6])
            # 7 - Local port
            local_port = parsing.parse_int(parts[7])
            return cls(
                up_since=up_since,
                state_name=state_name,
                desc_string=desc_string,
                local_virtual_v4_addr=local_virtual_v4_addr,
                remote_addr=remote_addr,
                remote_port=remote_port,
                local_addr=local_addr,
                local_port=local_port,
            )
        raise errors.ParseError("Did not get expected data from state.")

    def __repr__(self) -> str:
        return f"<State desc='{self.desc_string}', mode='{self.mode}'>"
