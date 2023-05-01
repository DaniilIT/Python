import socket
from collections import deque
from select import select

# David Beazley
# 2015 PyCon
# Concurrency from the Ground up Live
# Конкурентность в Python с 0 в живую

tasks = deque([])  # [<generator>, ...]
to_read = {}  # {server_socket: <generator>, ...}
to_write = {}


def server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 5000))
    server_socket.listen()

    while True:
        yield 'read', server_socket
        client_socket, addr = server_socket.accept()

        print('Connection from', addr)
        tasks.append(client(client_socket))


def client(client_socket):
    while True:
        yield 'read', client_socket
        request = client_socket.recv(4 * 1024)

        if not request:
            break
        else:
            response = 'Hello world!\n'.encode()

            yield 'write', client_socket
            client_socket.send(response)

    client_socket.close()


def event_loop():
    tasks.append(server())  # [<generator>, ...]

    while any([tasks, to_read, to_write]):

        while not tasks:
            ready_to_read, ready_to_write, _ = select(to_read, to_write, [])  # переберет ключи, т. е. сокеты

            for sock in ready_to_read:
                tasks.append(to_read.pop(sock))  # <generator>

            for sock in ready_to_write:
                tasks.append(to_write.pop(sock))

        try:
            task = tasks.popleft()
            reason, sock = next(task)

            if reason == 'read':
                to_read[sock] = task
            elif reason == 'write':
                to_write[sock] = task
        except StopIteration:
            print('Done!')


if __name__ == '__main__':
    event_loop()
