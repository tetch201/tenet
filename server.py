import logging
import sys
from websockets.sync.server import serve
from websockets.exceptions import WebSocketException

logging.basicConfig(level=logging.INFO)

connected_clients = set()
users = {}

def echo(websocket):
    try:
        user = websocket.recv()
        users[websocket] = user
        connected_clients.add(websocket)
        logging.info(f'Клиент подключен: {user} {websocket.remote_address}')
        
        while True:
            message = websocket.recv()
            if message:
                for client in connected_clients:
                    if client != websocket:
                        client.send(f"{user}: {message}")
    except WebSocketException:
        logging.info(f"Клиент отключен: {user}")
    finally:
        if websocket in connected_clients:
            connected_clients.remove(websocket)
        if websocket in users:
            del users[websocket]

def main(port):
    with serve(echo, "localhost", port) as server:
        server.serve_forever()

if __name__ == "__main__":
    port = int(sys.argv[1])
    main(port)