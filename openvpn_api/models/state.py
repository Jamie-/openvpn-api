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

class State:
    up_since = None  # Datetime daemon started?
    state_name = None  # See states list above
    desc_string = None
    local_virtual_v4_addr = None
    remote_addr = None
    remote_port = None
    local_addr = None
    local_port = None
    local_virtual_v6_addr = None

    def __init__(self,
                 up_since=None,
                 state_name=None,
                 desc_string=None,
                 local_virtual_v4_addr=None,
                 remote_addr=None,
                 remote_port=None,
                 local_addr=None,
                 local_port=None,
                 local_virtual_v6_addr=None):
        if up_since is not None:
            self.up_since = datetime.datetime.utcfromtimestamp(int(up_since))
        if state_name is not None:
            self.state_name = state_name
        if desc_string is not None:
            self.desc_string = desc_string
        if local_virtual_v4_addr is not None:
            self.local_virtual_v4_addr = local_virtual_v4_addr
        if remote_addr is not None:
            self.remote_addr = remote_addr
        if remote_port is not None:
            self.remote_port = int(remote_port)
        if local_addr is not None:
            self.local_addr = local_addr
        if local_port is not None:
            self.local_port = int(local_port)
        if local_virtual_v6_addr is not None:
            self.local_virtual_v6_addr = local_virtual_v6_addr

    @property
    def mode(self):
        if self.remote_addr is None and self.local_addr is None:
            return 'unknown'
        if self.remote_addr is None:
            return 'server'
        return 'client'
