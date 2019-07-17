
class ServerStats:
    client_count = None  # Number of connected clients
    bytes_in = None  # Server bytes in
    bytes_out = None  # Server bytes out

    def __init__(self,
                 client_count=None,
                 bytes_in=None,
                 bytes_out=None):
        if client_count:
            self.client_count = int(client_count)
        if bytes_in:
            self.bytes_in = int(bytes_in)
        if bytes_out:
            self.bytes_out = int(bytes_out)

    def __repr__(self):
        return '<ServerStats client_count={}, bytes_in={}, bytes_out={}>'.format(self.client_count, self.bytes_in, self.bytes_out)
