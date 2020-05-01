from typing import Optional


class ServerStats:
    """OpenVPN server stats model."""

    def __init__(
        self, client_count: Optional[int] = None, bytes_in: Optional[int] = None, bytes_out: Optional[int] = None,
    ) -> None:
        # Number of connected clients
        self.client_count = int(client_count) if client_count else None  # type: int
        # Server bytes in
        self.bytes_in = int(bytes_in) if bytes_in else None  # type: int
        # Server bytes out
        self.bytes_out = int(bytes_out) if bytes_out else None  # type: int

    def __repr__(self) -> str:
        return f"<ServerStats client_count={self.client_count}, bytes_in={self.bytes_in}, bytes_out={self.bytes_out}>"
