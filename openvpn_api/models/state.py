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

from openvpn_api.models import VPNModelBase
from openvpn_api.util import errors


class State(VPNModelBase):
    """OpenVPN daemon state model."""

    def __init__(
        self,
        up_since: Optional[datetime.datetime] = None,
        state_name: Optional[str] = None,
        desc_string: Optional[str] = None,
        local_virtual_v4_addr: Optional[netaddr.IPAddress] = None,
        remote_addr: Optional[netaddr.IPAddress] = None,
        remote_port: Optional[int] = None,
        local_addr: Optional[netaddr.IPAddress] = None,
        local_port: Optional[int] = None,
        local_virtual_v6_addr: Optional[str] = None,
    ) -> None:
        # Datetime daemon started?
        self.up_since = up_since  # type: Optional[datetime.datetime]
        # See states list in module docstring
        self.state_name = state_name  # type: Optional[str]
        self.desc_string = desc_string  # type: Optional[str]
        self.local_virtual_v4_addr = local_virtual_v4_addr  # type: Optional[netaddr.IPAddress]
        self.remote_addr = remote_addr  # type: Optional[netaddr.IPAddress]
        self.remote_port = remote_port  # type: Optional[int]
        self.local_addr = local_addr  # type: Optional[netaddr.IPAddress]
        self.local_port = local_port  # type: Optional[int]
        self.local_virtual_v6_addr = local_virtual_v6_addr  # type: Optional[str]

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
            if line.startswith(">INFO") or line.startswith(">CLIENT") or line.startswith(">STATE"):
                continue
            if line.strip() == "END":
                break
            parts = line.split(",")
            # 0 - Unix timestamp of server start (UTC?)
            up_since = datetime.datetime.utcfromtimestamp(int(parts[0])) if parts[0] != "" else None
            # 1 - Connection state
            state_name = cls._parse_string(parts[1])
            # 2 - Connection state description
            desc_string = cls._parse_string(parts[2])
            # 3 - TUN/TAP local v4 address
            local_virtual_v4_addr = cls._parse_ipv4(parts[3])
            # 4 - Remote server address (client only)
            remote_addr = cls._parse_ipv4(parts[4])
            # 5 - Remote server port (client only)
            remote_port = cls._parse_int(parts[5])
            # 6 - Local address
            local_addr = cls._parse_ipv4(parts[6])
            # 7 - Local port
            local_port = cls._parse_int(parts[7])
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
