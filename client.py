import time
import logging
import sys
import threading
from websockets.sync.client import connect
from websockets.exceptions import WebSocketException

logging.basicConfig(level=logging.INFO)

def receive_messages(websocket):
    while True:
        try:
            message = websocket.recv()
            if message is None:
                break
            print(f"{message}")
        except WebSocketException as e:
            logging.error(f"Ошибка при получении сообщения: {e}")
            break
def send_message(websocket):
    while True:
        message = input()
        if message.strip() == "":
            continue
        try:
            websocket.send(message)
        except WebSocketException as e:
            logging.error(f"Ошибка при отправке сообщения: {e}")
            break
def send_username(websocket, username):
    try:
        websocket.send(username)
        threading.Thread(target=receive_messages, args=(websocket,), daemon=True).start()
        send_message(websocket)
    except WebSocketException as e:
        logging.error(f"Ошибка при отправке имени пользователя: {e}")
        return

def conn(ws_tunnel, username):
    while True:
        try:
            with connect(ws_tunnel, user_agent_header="WebSocket Python request!") as websocket:
                print('Соединение успешно.')
                send_username(websocket, username)
                break
        except WebSocketException as e:
            logging.error(f"Ошибка подключения: {e}. Повторная попытка через 3 секунды...")
            time.sleep(3)

if __name__ == '__main__':
    if len(sys.argv) == 2:
        ws_tunnel = sys.argv[1]
    else:
        ws_tunnel = input('Введите адрес сервера:')
    username = input('Введите ваш username:')
    conn(ws_tunnel, username)
