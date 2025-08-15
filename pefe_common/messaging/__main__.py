import sys
import time
from .json import *

usage = """
Usage:

python -m pefe_common.messaging <mode> <host> <port>

where
    <mode> is server or client,
    <host> and <port> form the server address, either to bind to (in
        case <mode> is server) or to connect to (in case <mode> is
        client).
"""

def main():
    if len(sys.argv) < 4:
        print(usage)
        return 1
    
    _, mode, host, port = sys.argv[:4]
    port = int(port)
    if mode == 'server':
        class ExampleJSONServer(JSONServer):
            def handle_client(self, conn, addr):
                print("Client connected from", addr)
                try:
                    while True:
                        msg = conn.recv_json()  # receive a Python object
                        print(f"Received from [{addr}]:", msg)

                        # Echo back with a server tag
                        conn.send_json({"server_echo": msg})
                except ConnectionError:
                    print("Client disconnected", addr)
        
        server = ExampleJSONServer(host, port)
        server.start()
        print(f"Server started on {host}:{port}")

        try:
            while True:
                time.sleep(3600)
        except KeyboardInterrupt:
            print()
            print("Stopping server... ", end="", flush=True)
            server.stop()
            print("Done.")
    
    elif mode == 'client':
        client = JSONClient(host, port)
        for i in range(5):
            msg = {"count": i, "message": "Hello from client"}
            print("Sending:", msg)
            client.send_json(msg)

            reply = client.recv_json()
            print("Reply from server:", reply)

            time.sleep(1)

        client.close()

    else:
        print(f"Invalid mode: {mode}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
