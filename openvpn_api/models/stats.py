import re
from typing import Optional

from openvpn_api.models import VPNModelBase
from openvpn_api.util import errors


class ServerStats(VPNModelBase):
    """OpenVPN server stats model."""

    def __init__(self, client_count: int = None, bytes_in: int = None, bytes_out: int = None,) -> None:
        # Number of connected clients
        self.client_count: Optional[int] = client_count
        # Server bytes in
        self.bytes_in: Optional[int] = bytes_in
        # Server bytes out
        self.bytes_out: Optional[int] = bytes_out

    @classmethod
    def parse_raw(cls, raw: str) -> "ServerStats":
        """Parse raw `load-stats` response into an instance."""
        for line in raw.splitlines():
            if not line.startswith("SUCCESS"):
                continue
            match = re.search(
                r"SUCCESS: nclients=(?P<nclients>\d+),bytesin=(?P<bytesin>\d+),bytesout=(?P<bytesout>\d+)", line
            )
            if not match:
                raise errors.ParseError("Unable to parse stats from raw load-stats response.")
            return cls(
                client_count=int(match.group("nclients")),
                bytes_in=int(match.group("bytesin")),
                bytes_out=int(match.group("bytesout")),
            )
        raise errors.ParseError("Did not get expected data from load-stats.")

    def __repr__(self) -> str:
        return f"<ServerStats client_count={self.client_count}, bytes_in={self.bytes_in}, bytes_out={self.bytes_out}>"
