import socket
import threading
import struct


class FramedSocket:
    """
    Length-prefixed framing over a socket.
    Default: 2-byte unsigned big-endian length (max payload 65535 bytes).
    """
    def __init__(self, sock, length_bytes=2, recv_timeout=None):
        if length_bytes not in (2, 4):
            raise ValueError("length_bytes must be 2 or 4")
        self._sock = sock
        self._length_bytes = length_bytes
        self._len_fmt = "!H" if length_bytes == 2 else "!I"
        self._lock = threading.Lock()
        if recv_timeout is not None:
            self._sock.settimeout(recv_timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()

    def _recvn(self, n):
        data = bytearray()
        while len(data) < n:
            chunk = self._sock.recv(n - len(data))
            if not chunk:
                raise ConnectionError("Connection closed by peer")
            data += chunk
        return bytes(data)

    def send_frame(self, payload):
        if not isinstance(payload, (bytes, bytearray, memoryview)):
            raise TypeError("payload must be bytes-like")

        max_len = 0xFFFF if self._length_bytes == 2 else 0xFFFFFFFF
        n = len(payload)
        if n > max_len:
            raise ValueError("Payload too large for {}-byte length prefix".format(self._length_bytes))

        header = struct.pack(self._len_fmt, n)
        with self._lock:
            self._sock.sendall(header + payload)

    def recv_frame(self):
        header = self._recvn(self._length_bytes)
        length, = struct.unpack(self._len_fmt, header)
        if length == 0:
            return b""
        return self._recvn(length)

    def settimeout(self, timeout):
        self._sock.settimeout(timeout)

    def fileno(self):
        return self._sock.fileno()

    def close(self):
        try:
            self._sock.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        try:
            self._sock.close()
        except Exception:
            pass
