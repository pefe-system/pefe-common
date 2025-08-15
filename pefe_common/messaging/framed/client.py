import socket
from .socket import FramedSocket

class FramedClient(FramedSocket):
    """
    Simple client that connects to a framed server.
    """
    def __init__(self, host, port, length_bytes=2, recv_timeout=None):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        super(FramedClient, self).__init__(sock, length_bytes=length_bytes, recv_timeout=recv_timeout)
