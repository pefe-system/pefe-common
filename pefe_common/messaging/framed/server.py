import socket
import threading
from .socket import FramedSocket

class FramedServer:
    """
    Threaded length-prefixed server.
    """
    def __init__(self, host, port, backlog=128, length_bytes=2, recv_timeout=None,
                 on_client=None, make_conn=None, reuse_addr=True, reuse_port=False):
        self._host = host
        self._port = port
        self._backlog = backlog
        self._length_bytes = length_bytes
        self._recv_timeout = recv_timeout
        self._on_client_cb = on_client
        self._make_conn = make_conn or (lambda s: FramedSocket(s, length_bytes=length_bytes, recv_timeout=recv_timeout))
        self._reuse_addr = reuse_addr
        self._reuse_port = reuse_port

        self._lsock = None
        self._accept_thread = None
        self._clients_lock = threading.Lock()
        self._clients = set()
        self._stop_event = threading.Event()

    def start(self):
        if self._lsock:
            raise RuntimeError("Server already started")

        self._lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self._reuse_addr:
            self._lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if self._reuse_port and hasattr(socket, "SO_REUSEPORT"):
            self._lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        self._lsock.bind((self._host, self._port))
        self._lsock.listen(self._backlog)

        self._accept_thread = threading.Thread(target=self._accept_loop, daemon=True)
        self._accept_thread.start()

    def _accept_loop(self):
        while not self._stop_event.is_set():
            try:
                client_sock, addr = self._lsock.accept()
            except OSError:
                break
            conn = self._make_conn(client_sock)
            t = threading.Thread(target=self._client_thread, args=(conn, addr), daemon=True)
            with self._clients_lock:
                self._clients.add(t)
            t.start()

    def _client_thread(self, conn, addr):
        try:
            if self._on_client_cb:
                self._on_client_cb(self, conn, addr)
            else:
                self.handle_client(conn, addr)
        except Exception:
            pass
        finally:
            conn.close()
            with self._clients_lock:
                self._clients.discard(threading.current_thread())

    def handle_client(self, conn, addr):
        """Override in subclass."""
        raise NotImplementedError

    def stop(self):
        self._stop_event.set()
        if self._lsock:
            try:
                self._lsock.close()
            except Exception:
                pass
        if self._accept_thread:
            self._accept_thread.join(timeout=1)
        with self._clients_lock:
            for t in list(self._clients):
                t.join(timeout=1)
