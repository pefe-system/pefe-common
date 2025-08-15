import json
from ..framed import FramedSocket

class JSONSocket(FramedSocket):
    """
    A FramedSocket that (de)serializes JSON payloads.
    """
    def __init__(self, sock, length_bytes=2, recv_timeout=None, ensure_ascii=False):
        super(JSONSocket, self).__init__(sock, length_bytes=length_bytes, recv_timeout=recv_timeout)
        self._ensure_ascii = ensure_ascii

    def send_json(self, obj):
        text = json.dumps(obj, ensure_ascii=self._ensure_ascii, separators=(",", ":"))
        self.send_frame(text.encode("utf-8"))

    def recv_json(self):
        data = self.recv_frame()
        return json.loads(data.decode("utf-8"))
