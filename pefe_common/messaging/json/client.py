import socket
from .socket import JSONSocket

class JSONClient(JSONSocket):
    """
    Simple client that connects to a JSON server.
    """
    def __init__(self, host, port, length_bytes=2, recv_timeout=None, ensure_ascii=False):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        super(JSONClient, self).__init__(sock, length_bytes=length_bytes,
                                         recv_timeout=recv_timeout,
                                         ensure_ascii=ensure_ascii)
