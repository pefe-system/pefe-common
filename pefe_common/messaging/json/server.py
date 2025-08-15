from ..framed.server import FramedServer
from .socket import JSONSocket

class JSONServer(FramedServer):
    """
    A FramedServer that uses JSONSocket for client connections.
    """
    def __init__(self, host, port, backlog=128, length_bytes=2, recv_timeout=None,
                 on_client=None, ensure_ascii=False):
        def make_json_conn(sock):
            return JSONSocket(sock, length_bytes=length_bytes, recv_timeout=recv_timeout,
                              ensure_ascii=ensure_ascii)
        super(JSONServer, self).__init__(host, port, backlog=backlog,
                                         length_bytes=length_bytes,
                                         recv_timeout=recv_timeout,
                                         on_client=on_client,
                                         make_conn=make_json_conn)
