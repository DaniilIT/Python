import socket
from select import select

to_monitor = []

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # (IP4, TCP)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # переиспользование порта
server_socket.bind(('localhost', 5000))  # привязка к домену
server_socket.listen()  # прослушивание на предмет входящих подключений


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()  # ждем входящего подключения (блокирующая операция)
    print('Connection from', addr)  # Connection from ('127.0.0.1', 62619)

    to_monitor.append(client_socket)


# низкая связность между блокирующими функциями

def send_message(client_socket):
    request = client_socket.recv(4 * 1024)  # ждет сообщение от клиента

    if request:
        response = 'Hello world!\n'.encode()
        client_socket.send(response)
    else:
        to_monitor.remove(client_socket)
        client_socket.close()


def event_loop():
    to_monitor.append(server_socket)

    while True:
        ready_to_read, _, _ = select(to_monitor, [], [])  # доступны для read, write, errors

        for sock in ready_to_read:
            if sock is server_socket:
                accept_connection(sock)
            else:
                send_message(sock)


if __name__ == '__main__':
    event_loop()
