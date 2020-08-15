import contextlib
import logging
import re
import socket
from enum import Enum
from typing import Optional, Generator

import openvpn_status
from openvpn_status.models import Status

from openvpn_api.models.state import State
from openvpn_api.models.stats import ServerStats
from openvpn_api.util import errors

logger = logging.getLogger(__name__)


class VPNType(str, Enum):
    IP = "ip"
    UNIX_SOCKET = "socket"


class VPN:
    def __init__(self, host: str = None, port: int = None, unix_socket: str = None):
        if (unix_socket and host) or (unix_socket and port) or (not unix_socket and not host and not port):
            raise errors.VPNError("Must specify either socket or host and port")

        self._release: Optional[str] = None
        self._mgmt_socket: Optional[str] = unix_socket
        self._mgmt_host: Optional[str] = host
        self._mgmt_port: Optional[int] = port

        # release info and daemon state caches
        self._socket: Optional[socket.socket] = None

    @property
    def type(self) -> VPNType:
        """Get VPNType object for this VPN.
        """
        if self._mgmt_socket:
            return VPNType.UNIX_SOCKET
        if self._mgmt_port and self._mgmt_host:
            return VPNType.IP
        raise ValueError("Invalid connection type")

    @property
    def mgmt_address(self) -> str:
        """Get address of management interface.
        """
        if self.type == VPNType.IP:
            return f"{self._mgmt_host}:{self._mgmt_port}"
        else:
            return str(self._mgmt_socket)

    def connect(self) -> Optional[bool]:
        """Connect to management interface socket.
        """
        try:
            if self.type == VPNType.IP:
                assert self._mgmt_host is not None and self._mgmt_port is not None
                self._socket = socket.create_connection((self._mgmt_host, self._mgmt_port), timeout=3)
            elif self.type == VPNType.UNIX_SOCKET:
                assert self._mgmt_socket is not None
                self._socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._socket.connect(self._mgmt_socket)
            else:
                raise ValueError("Invalid connection type")

            resp = self._socket_recv()
            assert resp.startswith(">INFO"), "Did not get expected response from interface when opening socket."
            return True
        except (socket.timeout, socket.error) as e:
            raise errors.ConnectError(str(e)) from None

    def disconnect(self, _quit=True) -> None:
        """Disconnect from management interface socket.
        By default will issue the `quit` command to inform the management interface we are closing the connection
        """
        if self._socket is not None:
            if _quit:
                self._socket_send("quit\n")
            self._socket.close()
            self._socket = None

    @property
    def is_connected(self) -> bool:
        """Determine if management interface socket is connected or not.
        """
        return self._socket is not None

    @contextlib.contextmanager
    def connection(self) -> Generator:
        """Create context where management interface socket is open and close when done.
        """
        self.connect()
        try:
            yield
        finally:
            self.disconnect()

    def _socket_send(self, data) -> None:
        """Convert data to bytes and send to socket.
        """
        if self._socket is None:
            raise errors.NotConnectedError("You must be connected to the management interface to issue commands.")
        self._socket.send(bytes(data, "utf-8"))

    def _socket_recv(self) -> str:
        """Receive bytes from socket and convert to string.
        """
        if self._socket is None:
            raise errors.NotConnectedError("You must be connected to the management interface to issue commands.")
        return self._socket.recv(4096).decode("utf-8")

    def send_command(self, cmd) -> str:
        """Send command to management interface and fetch response.
        """
        logger.debug("Sending cmd: %r", cmd.strip())
        self._socket_send(cmd + "\n")
        resp = self._socket_recv()
        if cmd.strip() not in ("load-stats", "signal SIGTERM"):
            while not (resp.strip().endswith("END") or resp.strip().startswith("SUCCESS:")):
                resp += self._socket_recv()
        logger.debug("Cmd response: %r", resp)
        return resp

    # Interface commands and parsing

    def _get_version(self) -> str:
        """Get OpenVPN version from socket.
        """
        raw = self.send_command("version")
        for line in raw.splitlines():
            if line.startswith("OpenVPN Version"):
                return line.replace("OpenVPN Version: ", "")
        raise errors.ParseError("Unable to get OpenVPN version, no matches found in socket response.")

    @property
    def release(self) -> str:
        """OpenVPN release string.
        """
        if self._release is None:
            self._release = self._get_version()
        return self._release

    @property
    def version(self) -> Optional[str]:
        """OpenVPN version number.
        """
        if self.release is None:
            return None
        match = re.search(r"OpenVPN (?P<version>\d+.\d+.\d+)", self.release)
        if not match:
            raise errors.ParseError("Unable to parse version from release string.")
        return match.group("version")

    def get_state(self) -> State:
        """Get OpenVPN daemon state from socket.
        """
        raw = self.send_command("state")
        return State.parse_raw(raw)

    def cache_data(self) -> None:
        """Cached some metadata about the connection.
        """
        _ = self.release

    def clear_cache(self) -> None:
        """Clear cached state data about connection.
        """
        self._release = None

    def send_sigterm(self) -> None:
        """Send a SIGTERM to the OpenVPN process.
        """
        raw = self.send_command("signal SIGTERM")
        if raw.strip() != "SUCCESS: signal SIGTERM thrown":
            raise errors.ParseError("Did not get expected response after issuing SIGTERM.")
        self.disconnect(_quit=False)

    def get_stats(self) -> ServerStats:
        """Get latest VPN stats.
        """
        raw = self.send_command("load-stats")
        return ServerStats.parse_raw(raw)

    def get_status(self) -> Status:
        """Get current status from VPN.

        Uses openvpn-status library to parse status output:
        https://pypi.org/project/openvpn-status/
        """
        raw = self.send_command("status 1")
        return openvpn_status.parse_status(raw)
